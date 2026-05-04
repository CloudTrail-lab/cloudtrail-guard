from __future__ import annotations
from typing import Any
from app.services.timeline_builder import STAGE_MAP


def _risk_label(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _node_id(value: str) -> str:
    return value.replace(":", "_").replace("/", "_").replace(".", "_").replace("-", "_")[:80]


def _target_from_event(event: dict[str, Any]) -> tuple[str, str, str]:
    params = event.get("requestParameters") or {}
    name = event["eventName"]
    if name in {"CreateUser", "AttachUserPolicy", "PutUserPolicy"}:
        label = params.get("userName", "iam-user")
        return f"user_{_node_id(label)}", "user", label
    if name == "AssumeRole":
        role_arn = params.get("roleArn", "iam-role")
        label = role_arn.split("/")[-1]
        return f"role_{_node_id(label)}", "iam_role", label
    if name in {"GetObject", "PutBucketPolicy"}:
        label = params.get("bucketName", "s3-bucket")
        return f"s3_{_node_id(label)}", "s3", label
    if name == "AuthorizeSecurityGroupIngress":
        label = params.get("groupId", "security-group")
        return f"sg_{_node_id(label)}", "ec2", label
    if name in {"StopLogging", "DeleteTrail"}:
        label = params.get("name", "cloudtrail")
        return f"trail_{_node_id(label)}", "cloudtrail", label
    return f"api_{_node_id(name)}", "api", name


def reconstruct_attack(alert: dict[str, Any], events: list[dict[str, Any]]) -> dict[str, Any]:
    related_ids = set(alert.get("related_events") or [])
    related = [event for event in events if event["eventID"] in related_ids]
    if not related and events:
        related = sorted(events, key=lambda event: event["risk_score"], reverse=True)[:5]
    related.sort(key=lambda event: event.get("eventTime", ""))

    nodes: dict[str, dict[str, Any]] = {}
    edges: list[dict[str, Any]] = []
    kill_chain: list[dict[str, Any]] = []

    for event in related:
        principal = event.get("principal", "unknown")
        source_id = f"principal_{_node_id(principal)}"
        nodes.setdefault(source_id, {
            "id": source_id,
            "type": "user",
            "label": principal,
            "risk_score": event["risk_score"],
            "arn": event.get("userIdentity", {}).get("arn"),
        })
        nodes[source_id]["risk_score"] = max(nodes[source_id]["risk_score"], event["risk_score"])

        target_id, target_type, target_label = _target_from_event(event)
        nodes.setdefault(target_id, {
            "id": target_id,
            "type": target_type,
            "label": target_label,
            "risk_score": event["risk_score"],
            "arn": None,
        })
        nodes[target_id]["risk_score"] = max(nodes[target_id]["risk_score"], event["risk_score"])

        edges.append({
            "source": source_id,
            "target": target_id,
            "action": event["eventName"],
            "timestamp": event["eventTime"],
            "risk": _risk_label(event["risk_score"]),
            "event_id": event["eventID"],
        })
        kill_chain.append({
            "stage": STAGE_MAP.get(event["eventName"], "Activity"),
            "events": [event["eventID"]],
            "timestamp": event["eventTime"],
            "description": event.get("anomaly_reason") or f"{event['eventName']} observed",
            "risk": _risk_label(event["risk_score"]),
        })

    return {
        "alert_id": alert.get("alert_id"),
        "nodes": list(nodes.values()),
        "edges": edges,
        "kill_chain": kill_chain,
    }

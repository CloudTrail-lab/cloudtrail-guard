from __future__ import annotations
from collections import defaultdict
from typing import Any


def _evidence_for_event(event: dict[str, Any]) -> list[dict[str, Any]]:
    evidence = [
        {"feature": "eventName", "value": event["eventName"], "importance": min(1.0, event["risk_score"] / 100)},
        {"feature": "sourceIPAddress", "value": event.get("sourceIPAddress", "unknown"), "importance": 0.55},
    ]
    if event.get("requestParameters"):
        evidence.append({"feature": "requestParameters", "value": str(event["requestParameters"])[:160], "importance": 0.75})
    return evidence


def generate_alerts(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    alerts: list[dict[str, Any]] = []

    for idx, event in enumerate(events, start=1):
        if event["risk_score"] < 70:
            continue
        alerts.append({
            "alert_id": f"alert-{idx:03d}",
            "user_id": event.get("principal", "unknown"),
            "detection_method": "rule",
            "rule_id": event.get("rule_id", "rule-high-risk-event"),
            "rule_name": event.get("anomaly_reason") or "High-risk CloudTrail event",
            "risk_score": event["risk_score"],
            "status": "new",
            "detected_at": event["eventTime"],
            "summary": f"High-risk API call detected: {event['eventName']} by {event.get('principal', 'unknown')}",
            "related_events": [event["eventID"]],
            "evidence": _evidence_for_event(event),
            "suppressed": False,
        })

    alerts.extend(_generate_correlated_privilege_alerts(events, len(alerts) + 1))
    return sorted(alerts, key=lambda alert: (alert["risk_score"], alert["detected_at"]), reverse=True)


def _generate_correlated_privilege_alerts(events: list[dict[str, Any]], start_idx: int) -> list[dict[str, Any]]:
    by_principal: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for event in events:
        by_principal[event.get("principal", "unknown")].append(event)

    correlated: list[dict[str, Any]] = []
    idx = start_idx
    for principal, principal_events in by_principal.items():
        names = [event["eventName"] for event in principal_events]
        if "CreateUser" in names and "AttachUserPolicy" in names:
            related = [event for event in principal_events if event["eventName"] in {"ConsoleLogin", "CreateUser", "AttachUserPolicy", "AssumeRole", "GetObject"}]
            if not related:
                continue
            max_risk = max(event["risk_score"] for event in related)
            correlated.append({
                "alert_id": f"alert-{idx:03d}",
                "user_id": principal,
                "detection_method": "rule",
                "rule_id": "rule-privilege-escalation-sequence",
                "rule_name": "Privilege Escalation Sequence",
                "risk_score": max(95, max_risk),
                "status": "new",
                "detected_at": related[-1]["eventTime"],
                "summary": "Privilege escalation sequence detected: ConsoleLogin/CreateUser/AttachUserPolicy activity chain.",
                "related_events": [event["eventID"] for event in related],
                "evidence": [
                    {"feature": "API sequence", "value": " → ".join(event["eventName"] for event in related), "importance": 0.92},
                    {"feature": "principal", "value": principal, "importance": 0.75},
                    {"feature": "event_count", "value": str(len(related)), "importance": 0.68},
                ],
                "suppressed": False,
            })
            idx += 1
    return correlated

from __future__ import annotations
from typing import Any
from app.services.risk_engine import evaluate_record


def principal_from_identity(identity: dict[str, Any]) -> str:
    if not identity:
        return "unknown"
    if identity.get("userName"):
        return identity["userName"]
    session_issuer = identity.get("sessionContext", {}).get("sessionIssuer", {})
    if session_issuer.get("userName"):
        return session_issuer["userName"]
    arn = identity.get("arn", "")
    if "/" in arn:
        return arn.split("/")[-1]
    return identity.get("principalId", "unknown")


def normalize_record(record: dict[str, Any], index: int = 0) -> dict[str, Any]:
    risk = evaluate_record(record)
    identity = record.get("userIdentity") or {}
    event_id = record.get("eventID") or f"evt-{index + 1:06d}"

    return {
        "eventID": event_id,
        "eventName": record.get("eventName", "Unknown"),
        "eventTime": record.get("eventTime", "1970-01-01T00:00:00Z"),
        "userIdentity": identity,
        "principal": principal_from_identity(identity),
        "sourceIPAddress": record.get("sourceIPAddress", "unknown"),
        "userAgent": record.get("userAgent", "unknown"),
        "awsRegion": record.get("awsRegion", "unknown"),
        "eventSource": record.get("eventSource", "unknown"),
        "eventStatus": "Error" if record.get("errorCode") else "Success",
        "risk_score": risk["risk_score"],
        "risk_level": risk["risk_level"],
        "requestParameters": record.get("requestParameters"),
        "responseElements": record.get("responseElements"),
        "anomaly_reason": risk["reason"] if risk["risk_score"] >= 40 else None,
        "raw": record,
        "rule_id": risk["rule_id"],
    }


def normalize_records(records: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [normalize_record(record, idx) for idx, record in enumerate(records)]

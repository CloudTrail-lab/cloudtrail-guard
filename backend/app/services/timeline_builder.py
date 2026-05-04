from __future__ import annotations
from datetime import datetime

STAGE_MAP = {
    "ConsoleLogin": "Initial Access",
    "CreateUser": "Preparation",
    "AttachUserPolicy": "Privilege Escalation",
    "PutUserPolicy": "Privilege Escalation",
    "CreateAccessKey": "Credential Access",
    "AssumeRole": "Lateral Movement",
    "GetObject": "Collection",
    "AuthorizeSecurityGroupIngress": "Persistence",
    "StopLogging": "Defense Evasion",
    "DeleteTrail": "Defense Evasion",
}


def _hhmm(timestamp: str) -> str:
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%H:%M")
    except Exception:
        return timestamp[11:16] if len(timestamp) >= 16 else timestamp


def build_timeline(events: list[dict], user_id: str) -> dict:
    related = [
        event for event in events
        if event.get("principal") == user_id
        or event.get("userIdentity", {}).get("userName") == user_id
        or user_id in str(event.get("requestParameters") or {})
    ]
    related.sort(key=lambda event: event.get("eventTime", ""))

    return {
        "user_id": user_id,
        "events": [
            {
                "id": event["eventID"],
                "time": _hhmm(event["eventTime"]),
                "timestamp": event["eventTime"],
                "event_name": event["eventName"],
                "status": event["eventStatus"],
                "risk_score": event["risk_score"],
                "is_anomaly": event["risk_score"] >= 70,
                "stage": STAGE_MAP.get(event["eventName"], "Activity"),
                "anomaly_reason": event.get("anomaly_reason"),
            }
            for event in related
        ],
    }

from __future__ import annotations
from typing import Any

BASE_RULES: dict[str, tuple[int, str, str]] = {
    "ConsoleLogin": (25, "rule-console-login", "Console login observed"),
    "CreateUser": (70, "rule-create-user", "IAM user creation detected"),
    "AttachUserPolicy": (90, "rule-attach-user-policy", "IAM policy attached to user"),
    "PutUserPolicy": (85, "rule-put-user-policy", "Inline IAM policy added"),
    "CreateAccessKey": (80, "rule-create-access-key", "Long-lived access key created"),
    "AssumeRole": (65, "rule-assume-role", "Role assumption observed"),
    "StopLogging": (95, "rule-stop-logging", "CloudTrail logging disabled"),
    "DeleteTrail": (100, "rule-delete-trail", "CloudTrail trail deleted"),
    "AuthorizeSecurityGroupIngress": (70, "rule-security-group-ingress", "Security group ingress modified"),
    "PutBucketPolicy": (75, "rule-put-bucket-policy", "S3 bucket policy modified"),
    "GetObject": (40, "rule-s3-get-object", "S3 object access observed"),
}


def risk_level(score: int) -> str:
    if score >= 90:
        return "critical"
    if score >= 70:
        return "high"
    if score >= 40:
        return "medium"
    return "low"


def _contains_admin_access(params: Any) -> bool:
    return "AdministratorAccess" in str(params or "")


def _opens_world_ssh(params: Any) -> bool:
    text = str(params or "")
    return "0.0.0.0/0" in text and ("22" in text or "ssh" in text.lower())


def evaluate_record(record: dict[str, Any]) -> dict[str, Any]:
    event_name = record.get("eventName", "Unknown")
    params = record.get("requestParameters") or {}
    score, rule_id, reason = BASE_RULES.get(event_name, (20, "rule-low-risk-event", "Low-risk API call observed"))

    if event_name == "AttachUserPolicy" and _contains_admin_access(params):
        score = 95
        rule_id = "rule-admin-policy-attach"
        reason = "AdministratorAccess policy attached to IAM user"

    if event_name == "AuthorizeSecurityGroupIngress" and _opens_world_ssh(params):
        score = 85
        rule_id = "rule-open-security-group"
        reason = "Security group opened SSH access to 0.0.0.0/0"

    if "errorCode" in record:
        # Failed attempts are important but less severe than successful destructive actions.
        score = max(35, min(score - 20, 75))
        reason = f"Failed API attempt: {record.get('errorCode')}"

    return {
        "risk_score": max(0, min(100, score)),
        "risk_level": risk_level(score),
        "rule_id": rule_id,
        "reason": reason,
    }

# Data Schema

## NormalizedEvent

```json
{
  "eventID": "evt-001",
  "eventName": "CreateUser",
  "eventTime": "2026-05-02T10:05:00Z",
  "userIdentity": {},
  "principal": "admin-role",
  "sourceIPAddress": "203.0.113.45",
  "userAgent": "aws-cli/2.15.0",
  "awsRegion": "us-east-1",
  "eventSource": "iam.amazonaws.com",
  "eventStatus": "Success",
  "risk_score": 70,
  "risk_level": "high",
  "anomaly_reason": "IAM user creation detected",
  "requestParameters": {},
  "responseElements": {}
}
```

## Alert

```json
{
  "alert_id": "alert-001",
  "user_id": "admin-role",
  "detection_method": "rule",
  "rule_id": "rule-privilege-escalation",
  "risk_score": 95,
  "status": "new",
  "summary": "Privilege escalation detected",
  "related_events": ["evt-002", "evt-003"],
  "evidence": []
}
```

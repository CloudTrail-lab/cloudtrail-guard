from typing import Any, Literal
from pydantic import BaseModel, Field


class Evidence(BaseModel):
    feature: str
    value: str
    importance: float = Field(ge=0, le=1)


class NormalizedEvent(BaseModel):
    eventID: str
    eventName: str
    eventTime: str
    userIdentity: dict[str, Any] = Field(default_factory=dict)
    principal: str = "unknown"
    sourceIPAddress: str = "unknown"
    userAgent: str = "unknown"
    awsRegion: str = "unknown"
    eventSource: str = "unknown"
    eventStatus: Literal["Success", "Error"] = "Success"
    risk_score: int = Field(ge=0, le=100)
    risk_level: Literal["low", "medium", "high", "critical"]
    requestParameters: dict[str, Any] | None = None
    responseElements: Any = None
    anomaly_reason: str | None = None
    raw: dict[str, Any] = Field(default_factory=dict)


class Alert(BaseModel):
    alert_id: str
    user_id: str
    detection_method: Literal["rule", "ai"] = "rule"
    rule_id: str | None = None
    rule_name: str | None = None
    risk_score: int = Field(ge=0, le=100)
    status: Literal["new", "in_progress", "resolved"] = "new"
    detected_at: str
    summary: str
    related_events: list[str] = Field(default_factory=list)
    evidence: list[Evidence] = Field(default_factory=list)
    suppressed: bool = False


class AlertStatusUpdate(BaseModel):
    status: Literal["new", "in_progress", "resolved"]


class TimelineEvent(BaseModel):
    id: str
    time: str
    timestamp: str
    event_name: str
    status: str
    risk_score: int
    is_anomaly: bool
    stage: str
    anomaly_reason: str | None = None


class GraphNode(BaseModel):
    id: str
    type: str
    label: str
    risk_score: int
    arn: str | None = None


class GraphEdge(BaseModel):
    source: str
    target: str
    action: str
    timestamp: str
    risk: str
    event_id: str


class KillChainStep(BaseModel):
    stage: str
    events: list[str]
    timestamp: str
    description: str
    risk: str

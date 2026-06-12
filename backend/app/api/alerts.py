from fastapi import APIRouter, HTTPException, Query
from app.schemas.data.mock_store import get_alerts, update_alert_status
from app.schemas.domain import AlertStatusUpdate

router = APIRouter(prefix="/api/alerts", tags=["alerts"])


@router.get("")
def list_alerts(
    status: str | None = None,
    method: str | None = None,
    min_risk: int = Query(0, ge=0, le=100),
):
    alerts = get_alerts()
    if status:
        alerts = [alert for alert in alerts if alert["status"] == status]
    if method:
        alerts = [alert for alert in alerts if alert["detection_method"] == method]
    alerts = [alert for alert in alerts if alert["risk_score"] >= min_risk]
    return {
        "status": "success",
        "data": alerts,
        "total_count": len(alerts),
        "new_count": len([a for a in alerts if a["status"] == "new"]),
        "in_progress_count": len([a for a in alerts if a["status"] == "in_progress"]),
        "resolved_count": len([a for a in alerts if a["status"] == "resolved"]),
    }


@router.patch("/{alert_id}/status")
def patch_alert_status(alert_id: str, payload: AlertStatusUpdate):
    alert = update_alert_status(alert_id, payload.status)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "data": alert}

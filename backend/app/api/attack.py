from fastapi import APIRouter, HTTPException
from app.schemas.data.mock_store import get_alerts, get_events
from app.services.attack_reconstructor import reconstruct_attack

router = APIRouter(prefix="/api/attack", tags=["attack"])


@router.get("/{alert_id}")
def attack_graph(alert_id: str):
    alert = next((item for item in get_alerts() if item["alert_id"] == alert_id), None)
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    return {"status": "success", "data": reconstruct_attack(alert, get_events())}

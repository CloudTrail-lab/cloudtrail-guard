from fastapi import APIRouter
from app.data.mock_store import get_alerts, get_events
from app.services.dashboard_builder import build_dashboard

router = APIRouter(prefix="/api/dashboard", tags=["dashboard"])


@router.get("/summary")
def dashboard_summary():
    return {"status": "success", "data": build_dashboard(get_events(), get_alerts())}

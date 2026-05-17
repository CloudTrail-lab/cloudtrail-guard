from fastapi import APIRouter
from app.data.mock_store import get_events
from app.services.timeline_builder import build_timeline

router = APIRouter(prefix="/api/timeline", tags=["timeline"])


@router.get("/{user_id}")
def user_timeline(user_id: str):
    return {"status": "success", "data": build_timeline(get_events(), user_id)}

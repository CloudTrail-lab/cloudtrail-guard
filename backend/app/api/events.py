from fastapi import APIRouter, File, HTTPException, Query, UploadFile
from app.schemas.data.mock_store import get_events, set_records, load_sample
from app.services.cloudtrail_parser import CloudTrailParseError, extract_records, load_json_bytes

router = APIRouter(prefix="/api/events", tags=["events"])


@router.get("")
def list_events(
    query: str | None = None,
    event_name: str | None = None,
    status: str | None = None,
    limit: int = Query(200, ge=1, le=1000),
):
    events = get_events()
    if query:
        q = query.lower()
        events = [event for event in events if q in str(event).lower()]
    if event_name:
        events = [event for event in events if event["eventName"] == event_name]
    if status:
        events = [event for event in events if event["eventStatus"] == status]
    return {"status": "success", "data": events[:limit], "total_count": len(events)}


@router.post("/upload")
async def upload_events(file: UploadFile = File(...)):
    try:
        payload = load_json_bytes(await file.read(), file.filename or "")
        records = extract_records(payload)
        result = set_records(records)
    except CloudTrailParseError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    return {"status": "success", "data": result}


@router.post("/load-sample")
def reload_sample():
    return {"status": "success", "data": load_sample()}

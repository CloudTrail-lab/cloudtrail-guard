from __future__ import annotations
from pathlib import Path
from app.services.cloudtrail_parser import extract_records, load_json_file
from app.services.normalizer import normalize_records
from app.services.alert_generator import generate_alerts

ROOT_DIR = Path(__file__).resolve().parents[4]
SAMPLE_PATH = ROOT_DIR / "sample-data" / "cloudtrail-privilege-escalation.json"

EVENTS: list[dict] = []
ALERTS: list[dict] = []


def set_records(records: list[dict]) -> dict:
    global EVENTS, ALERTS
    EVENTS = normalize_records(records)
    ALERTS = generate_alerts(EVENTS)
    return {"events": len(EVENTS), "alerts": len(ALERTS)}


def load_sample() -> dict:
    payload = load_json_file(SAMPLE_PATH)
    return set_records(extract_records(payload))


def get_events() -> list[dict]:
    if not EVENTS:
        load_sample()
    return EVENTS


def get_alerts() -> list[dict]:
    if not ALERTS:
        load_sample()
    return ALERTS


def update_alert_status(alert_id: str, status: str) -> dict | None:
    for alert in get_alerts():
        if alert["alert_id"] == alert_id:
            alert["status"] = status
            return alert
    return None

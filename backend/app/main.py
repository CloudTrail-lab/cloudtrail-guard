from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import alerts, attack, dashboard, events, timeline
from app.schemas.data.mock_store import load_sample

app = FastAPI(title="CloudTrace-Guard API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(dashboard.router)
app.include_router(events.router)
app.include_router(alerts.router)
app.include_router(timeline.router)
app.include_router(attack.router)


@app.on_event("startup")
def startup_load_sample() -> None:
    load_sample()


@app.get("/health")
def health():
    return {"status": "healthy", "service": "cloudtrace-guard-api"}

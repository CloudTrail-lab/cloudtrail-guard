from __future__ import annotations
from collections import Counter, defaultdict
from datetime import datetime


def _hour_bucket(timestamp: str) -> str:
    try:
        return datetime.fromisoformat(timestamp.replace("Z", "+00:00")).strftime("%H:00")
    except Exception:
        return timestamp[11:13] + ":00" if len(timestamp) >= 13 else "unknown"


def build_dashboard(events: list[dict], alerts: list[dict]) -> dict:
    current = max([event.get("risk_score", 0) for event in events], default=0)
    previous = max(0, current - 7)

    hist = defaultdict(int)
    risk_by_hour = defaultdict(list)
    service_counter = Counter()

    for event in events:
        hour = _hour_bucket(event.get("eventTime", ""))
        hist[hour] += 1
        risk_by_hour[hour].append(event.get("risk_score", 0))
        source = event.get("eventSource", "unknown")
        service = source.split(".")[0].upper() if source != "unknown" else "UNKNOWN"
        service_counter[service] += max(event.get("risk_score", 0), 1)

    risk_trend = [
        {"time": hour, "risk": round(sum(scores) / len(scores)), "events": hist[hour]}
        for hour, scores in sorted(risk_by_hour.items())
    ]

    event_histogram = [
        {"time": hour, "count": count}
        for hour, count in sorted(hist.items())
    ]

    total_signal = sum(service_counter.values()) or 1
    signal_distribution = [
        {"service": service, "value": round(value / total_signal * 100)}
        for service, value in service_counter.most_common(5)
    ]

    return {
        "risk_score": {
            "current": current,
            "previous": previous,
            "trend": "up" if current >= previous else "down",
        },
        "risk_trend": risk_trend,
        "event_histogram": event_histogram,
        "top_anomalies": sorted(alerts, key=lambda alert: alert["risk_score"], reverse=True)[:5],
        "signal_distribution": signal_distribution,
        "totals": {
            "events": len(events),
            "alerts": len(alerts),
            "principals": len(set(event.get("principal", "unknown") for event in events)),
            "source_ips": len(set(event.get("sourceIPAddress", "unknown") for event in events)),
        },
    }

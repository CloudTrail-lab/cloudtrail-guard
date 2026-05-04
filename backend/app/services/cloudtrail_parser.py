import gzip
import json
from pathlib import Path
from typing import Any


class CloudTrailParseError(ValueError):
    pass


def load_json_bytes(content: bytes, filename: str = "") -> dict[str, Any]:
    try:
        if filename.endswith(".gz"):
            content = gzip.decompress(content)
        data = json.loads(content.decode("utf-8"))
    except Exception as exc:
        raise CloudTrailParseError(f"Invalid CloudTrail JSON: {exc}") from exc

    if not isinstance(data, dict):
        raise CloudTrailParseError("CloudTrail payload must be a JSON object.")
    return data


def load_json_file(path: Path) -> dict[str, Any]:
    return load_json_bytes(path.read_bytes(), path.name)


def extract_records(payload: dict[str, Any]) -> list[dict[str, Any]]:
    records = payload.get("Records")
    if records is None:
        # Also allow a single record for quick testing.
        if "eventName" in payload and "eventTime" in payload:
            return [payload]
        raise CloudTrailParseError("CloudTrail JSON must contain a Records array.")
    if not isinstance(records, list):
        raise CloudTrailParseError("Records must be an array.")
    return [record for record in records if isinstance(record, dict)]

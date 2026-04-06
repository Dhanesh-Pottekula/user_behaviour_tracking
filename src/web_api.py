"""Local HTTP API for the web collector app.

This server does three jobs:

1. Accept labeled raw events captured by the React web app.
2. Persist those events into JSONL files that the training pipeline can reuse.
3. Run the existing streaming predictor so the app can show live model output.

The implementation uses only the Python standard library so the repo does not
need any additional backend dependencies.
"""

# Enable postponed evaluation of type annotations.
from __future__ import annotations

# JSON is used for request/response bodies and JSONL persistence.
import json
# UUIDs provide session ids when the client does not send one.
import uuid
# `dataclass` gives us a compact container for per-session state.
from dataclasses import dataclass
# `HTTPStatus` makes response codes easier to read.
from http import HTTPStatus
# Standard-library HTTP server primitives are enough for this local API.
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
# `Path` is used for filesystem operations.
from pathlib import Path
# Locks protect file appends and predictor state in a threaded server.
from threading import Lock
# `Any` and `Callable` help with request typing.
from typing import Any, Callable

# Import training labels, event types, and file locations.
from config import (
    BEHAVIOR_LABELS,
    CAPTURED_EVENTS_FILE,
    CAPTURED_SEGMENTS_FILE,
    EVENT_TYPES,
    RAW_DATA_DIR,
    SEGMENTS_DATA_DIR,
)
# Reuse the raw-event schema so stored data stays training-compatible.
from schemas import RawEvent
# Reuse the existing streaming predictor for live model feedback.
from stream_inference import StreamBehaviorPredictor


@dataclass
class SessionState:
    """Per-session runtime state cached by the API server."""

    # The labeled behavior the user selected for data collection.
    target_label: str
    # The predictor instance carrying GRU hidden state across events.
    predictor: StreamBehaviorPredictor
    # How many events have been recorded in this session.
    event_count: int = 0
    # How many segments have been closed in this session.
    segment_count: int = 0


# Lock used when writing events or segments to disk.
FILE_LOCK = Lock()
# Lock used when reading/updating the in-memory session map.
SESSION_LOCK = Lock()
# In-memory session cache keyed by session id.
SESSIONS: dict[str, SessionState] = {}


def ensure_storage_directories() -> None:
    """Create data directories the collector depends on."""

    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)
    SEGMENTS_DATA_DIR.mkdir(parents=True, exist_ok=True)


def append_jsonl(path: Path, payload: dict[str, Any]) -> None:
    """Append one JSON object as a line in a JSONL file."""

    with FILE_LOCK:
        with path.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps(payload) + "\n")


def json_error(message: str, status: HTTPStatus = HTTPStatus.BAD_REQUEST) -> tuple[int, dict[str, Any]]:
    """Create a JSON error response payload."""

    return status, {"ok": False, "error": message}


def get_or_create_session(session_id: str, target_label: str | None = None) -> SessionState:
    """Return an existing session state or create a fresh one."""

    with SESSION_LOCK:
        session = SESSIONS.get(session_id)
        if session is None:
            chosen_label = target_label or "normal"
            session = SessionState(
                target_label=chosen_label,
                predictor=StreamBehaviorPredictor(),
            )
            SESSIONS[session_id] = session
        elif target_label is not None:
            session.target_label = target_label
        return session


def close_session(session_id: str) -> dict[str, Any]:
    """Remove one session from memory and return a summary."""

    with SESSION_LOCK:
        session = SESSIONS.pop(session_id, None)
    if session is None:
        return {"session_id": session_id, "event_count": 0, "segment_count": 0}
    session.predictor.reset()
    return {
        "session_id": session_id,
        "event_count": session.event_count,
        "segment_count": session.segment_count,
    }


class CollectorRequestHandler(BaseHTTPRequestHandler):
    """Request handler exposing a small JSON API for the collector app."""

    server_version = "BehaviorCollectorAPI/0.1"

    def log_message(self, format: str, *args) -> None:
        """Keep request logging compact and readable."""

        super().log_message(format, *args)

    def _set_headers(self, status: int = HTTPStatus.OK) -> None:
        """Write common CORS and JSON response headers."""

        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def _read_json(self) -> dict[str, Any]:
        """Read and decode a JSON request body."""

        content_length = int(self.headers.get("Content-Length", "0"))
        raw_body = self.rfile.read(content_length) if content_length else b"{}"
        return json.loads(raw_body.decode("utf-8"))

    def _send_json(self, payload: dict[str, Any], status: int = HTTPStatus.OK) -> None:
        """Send a JSON response body."""

        self._set_headers(status)
        self.wfile.write(json.dumps(payload).encode("utf-8"))

    def _dispatch(self, handler: Callable[[dict[str, Any]], tuple[int, dict[str, Any]]]) -> None:
        """Read the request body, call a handler, and return JSON."""

        try:
            payload = self._read_json()
            status, response = handler(payload)
        except json.JSONDecodeError:
            status, response = json_error("Invalid JSON body")
        except Exception as exc:  # pragma: no cover - defensive local API guard
            status, response = json_error(f"Internal server error: {exc}", HTTPStatus.INTERNAL_SERVER_ERROR)
        self._send_json(response, status)

    def do_OPTIONS(self) -> None:  # noqa: N802 - required BaseHTTPRequestHandler name
        """Handle CORS preflight requests."""

        self._set_headers(HTTPStatus.NO_CONTENT)

    def do_GET(self) -> None:  # noqa: N802 - required BaseHTTPRequestHandler name
        """Handle read-only API routes."""

        if self.path == "/api/health":
            self._send_json({"ok": True, "status": "healthy"})
            return
        if self.path == "/api/config":
            self._send_json(
                {
                    "ok": True,
                    "labels": list(BEHAVIOR_LABELS),
                    "event_types": list(EVENT_TYPES),
                    "capture_file": str(CAPTURED_EVENTS_FILE),
                    "segment_file": str(CAPTURED_SEGMENTS_FILE),
                }
            )
            return
        self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)

    def do_POST(self) -> None:  # noqa: N802 - required BaseHTTPRequestHandler name
        """Handle write and inference API routes."""

        routes: dict[str, Callable[[dict[str, Any]], tuple[int, dict[str, Any]]]] = {
            "/api/session/start": self.handle_session_start,
            "/api/session/end": self.handle_session_end,
            "/api/event": self.handle_event,
            "/api/segment": self.handle_segment,
        }
        handler = routes.get(self.path)
        if handler is None:
            self._send_json({"ok": False, "error": "Not found"}, HTTPStatus.NOT_FOUND)
            return
        self._dispatch(handler)

    def handle_session_start(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """Start or reset one labeled data-collection session."""

        target_label = str(payload.get("target_label", "normal"))
        if target_label not in BEHAVIOR_LABELS:
            return json_error(f"Unknown target_label '{target_label}'")

        session_id = str(payload.get("session_id") or f"web_{uuid.uuid4().hex[:12]}")
        session = get_or_create_session(session_id, target_label=target_label)
        session.predictor.reset()
        session.event_count = 0
        session.segment_count = 0
        return HTTPStatus.OK, {
            "ok": True,
            "session_id": session_id,
            "target_label": session.target_label,
        }

    def handle_session_end(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """End a session and clear its hidden state from server memory."""

        session_id = str(payload.get("session_id", "")).strip()
        if not session_id:
            return json_error("session_id is required")
        summary = close_session(session_id)
        return HTTPStatus.OK, {"ok": True, **summary}

    def handle_event(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """Persist one captured event and return the current model prediction."""

        raw_event_payload = payload.get("event")
        if not isinstance(raw_event_payload, dict):
            return json_error("event object is required")

        session_id = str(raw_event_payload.get("session_id", "")).strip()
        if not session_id:
            return json_error("event.session_id is required")

        target_label = payload.get("target_label")
        if target_label is not None and target_label not in BEHAVIOR_LABELS:
            return json_error(f"Unknown target_label '{target_label}'")

        # Use the selected label as the stored training label if the event body
        # omitted one. This keeps the collected data directly trainable.
        if target_label and "label" not in raw_event_payload:
            raw_event_payload["label"] = target_label

        event = RawEvent.from_dict(raw_event_payload)
        if event.event_type not in EVENT_TYPES:
            return json_error(f"Unknown event_type '{event.event_type}'")
        if event.label not in BEHAVIOR_LABELS:
            return json_error(f"Unknown label '{event.label}'")

        session = get_or_create_session(session_id, target_label=event.label)
        prediction = session.predictor.predict_event(event)
        session.event_count += 1

        append_jsonl(
            CAPTURED_EVENTS_FILE,
            {
                **event.to_dict(),
                "source": "web_collector",
            },
        )

        return HTTPStatus.OK, {
            "ok": True,
            "prediction": prediction,
            "event_count": session.event_count,
            "session_id": session_id,
        }

    def handle_segment(self, payload: dict[str, Any]) -> tuple[int, dict[str, Any]]:
        """Persist one closed segment summary from the web app."""

        segment = payload.get("segment")
        if not isinstance(segment, dict):
            return json_error("segment object is required")

        session_id = str(segment.get("session_id", "")).strip()
        if not session_id:
            return json_error("segment.session_id is required")

        session = get_or_create_session(session_id, target_label=str(segment.get("target_label", "normal")))
        session.segment_count += 1
        append_jsonl(
            CAPTURED_SEGMENTS_FILE,
            {
                **segment,
                "source": "web_collector",
            },
        )

        return HTTPStatus.OK, {
            "ok": True,
            "session_id": session_id,
            "segment_count": session.segment_count,
        }


def run_server(host: str = "127.0.0.1", port: int = 8008) -> None:
    """Start the local collector API server."""

    ensure_storage_directories()
    server = ThreadingHTTPServer((host, port), CollectorRequestHandler)
    print(f"Collector API running at http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down collector API...")
    finally:
        server.server_close()


if __name__ == "__main__":
    run_server()

"""Shared event schema definitions.

The rest of the codebase passes around a `RawEvent` instead of free-form
dictionaries whenever possible. That makes the event contract more explicit and
keeps conversion logic in one place.
"""

# Enable modern type-hint behavior without evaluating annotations immediately.
from __future__ import annotations

# `dataclass` gives us a compact way to define a structured event record.
from dataclasses import asdict, dataclass


@dataclass(slots=True)
class RawEvent:
    """One user interaction event before model feature encoding."""

    # Unique session identifier used to group events belonging to one journey.
    session_id: str
    # Event time in milliseconds.
    timestamp_ms: int
    # Event category such as scroll, click, or idle.
    event_type: str
    # Horizontal location, usually for click/touch/navigation interactions.
    x: float = 0.0
    # Vertical location on the screen.
    y: float = 0.0
    # Scroll distance for scroll events.
    delta_y: float = 0.0
    # Scroll speed or similar motion intensity.
    velocity: float = 0.0
    # Change in velocity, useful for abrupt movement patterns.
    acceleration: float = 0.0
    # Scroll direction, normalized later into -1 / 0 / 1 style values.
    direction: int = 0
    # Pressure is mainly useful for touch interactions.
    pressure: float = 0.0
    # How long the interaction or idle state lasted.
    duration_ms: float = 0.0
    # How long the user waited before the event.
    dwell_before_ms: float = 0.0
    # Number of selected words for selection-style interactions.
    selection_word_count: float = 0.0
    # Behavior label used only during supervised training and evaluation.
    label: str = "normal"

    @classmethod
    def from_dict(cls, payload: dict) -> "RawEvent":
        """Build a strongly typed event from a loose dictionary payload."""

        return cls(
            session_id=str(payload["session_id"]),
            timestamp_ms=int(payload["timestamp_ms"]),
            event_type=str(payload["event_type"]),
            x=float(payload.get("x", 0.0)),
            y=float(payload.get("y", 0.0)),
            delta_y=float(payload.get("delta_y", 0.0)),
            velocity=float(payload.get("velocity", 0.0)),
            acceleration=float(payload.get("acceleration", 0.0)),
            direction=int(payload.get("direction", 0)),
            pressure=float(payload.get("pressure", 0.0)),
            duration_ms=float(payload.get("duration_ms", 0.0)),
            dwell_before_ms=float(payload.get("dwell_before_ms", 0.0)),
            selection_word_count=float(payload.get("selection_word_count", 0.0)),
            label=str(payload.get("label", "normal")),
        )

    def to_dict(self) -> dict:
        """Convert the dataclass back into a plain JSON-serializable dictionary."""

        return asdict(self)

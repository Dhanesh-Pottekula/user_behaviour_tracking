"""Feature engineering utilities shared by training and inference.

The most important rule in this file is consistency: the same feature order and
normalization logic must be used during preprocessing, training, streaming
inference, and ONNX deployment.
"""

# Enable postponed evaluation of type annotations.
from __future__ import annotations

# `Iterable` lets `pad_or_truncate` accept many sequence-like inputs.
from collections.abc import Iterable

# Import the shared configuration that defines feature names, limits, and sizes.
from config import (
    EVENT_TYPES,
    FEATURE_DIM,
    FEATURE_NAMES,
    LABEL_TO_ID,
    NORMALIZATION_LIMITS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SEQ_LEN,
    SESSION_IDLE_RESET_MS,
)
# Import the structured event representation consumed by the encoder.
from schemas import RawEvent


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    """Limit a value to a bounded numeric range."""

    return max(low, min(high, value))


def normalize_signed(value: float, scale: float) -> float:
    """Normalize a signed value into the range [-1, 1]."""

    # Guard against invalid scales to avoid division by zero.
    if scale <= 0:
        return 0.0
    # Divide by the reference scale and clamp the result.
    return clamp(value / scale, low=-1.0, high=1.0)


def event_type_one_hot(event_type: str) -> list[float]:
    """Encode an event type as a one-hot vector.

    One-hot encoding is used instead of raw integer ids so the model does not
    accidentally learn a fake ordinal relationship between categories.
    """

    return [1.0 if event_type == candidate else 0.0 for candidate in EVENT_TYPES]


def event_to_feature_vector(event: RawEvent, prev_timestamp_ms: int | None) -> list[float]:
    """Convert one raw event into the exact feature order expected by the model."""

    # Compute how much time elapsed since the previous event in the same stream.
    time_delta_ms = 0.0 if prev_timestamp_ms is None else max(0.0, event.timestamp_ms - prev_timestamp_ms)

    # Start with the one-hot categorical representation of the event type.
    feature_vector = event_type_one_hot(event.event_type)
    # Append all normalized continuous features in a fixed order.
    feature_vector.extend(
        [
            clamp(event.velocity / NORMALIZATION_LIMITS["velocity"]),
            normalize_signed(event.acceleration, NORMALIZATION_LIMITS["acceleration"]),
            clamp(float(event.direction), low=-1.0, high=1.0),
            clamp(event.delta_y / NORMALIZATION_LIMITS["delta_y"]),
            clamp(event.x / SCREEN_WIDTH),
            clamp(event.y / SCREEN_HEIGHT),
            clamp(event.pressure),
            clamp(event.duration_ms / NORMALIZATION_LIMITS["duration_ms"]),
            clamp(event.dwell_before_ms / NORMALIZATION_LIMITS["dwell_before_ms"]),
            clamp(event.selection_word_count / NORMALIZATION_LIMITS["selection_word_count"]),
            clamp(time_delta_ms / NORMALIZATION_LIMITS["time_delta_ms"]),
        ]
    )
    # Return the fully encoded feature vector for one time step.
    return feature_vector


def pad_or_truncate(sequence: Iterable[list[float]], seq_len: int = SEQ_LEN) -> list[list[float]]:
    """Force any sequence to the fixed length used by offline training."""

    # Convert the input into a real list so we can measure and slice it.
    items = list(sequence)
    # If the sequence is long enough, keep the most recent `seq_len` events.
    if len(items) >= seq_len:
        return items[-seq_len:]

    # If the sequence is too short, left-pad it with all-zero feature vectors.
    padding = [[0.0] * FEATURE_DIM for _ in range(seq_len - len(items))]
    # Padding on the left preserves the temporal order of the real events.
    return padding + items


def build_preprocessing_metadata() -> dict:
    """Build the metadata object saved alongside processed data and checkpoints."""

    return {
        "seq_len": SEQ_LEN,
        "feature_dim": FEATURE_DIM,
        "feature_names": FEATURE_NAMES,
        "labels": LABEL_TO_ID,
        "event_types": list(EVENT_TYPES),
        "normalization_limits": NORMALIZATION_LIMITS,
        "screen": {"width": SCREEN_WIDTH, "height": SCREEN_HEIGHT},
        "session_idle_reset_ms": SESSION_IDLE_RESET_MS,
    }

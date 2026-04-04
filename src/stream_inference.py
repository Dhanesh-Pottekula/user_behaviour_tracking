"""Streaming inference helper for event-by-event behavior prediction."""

# Enable postponed type-annotation evaluation.
from __future__ import annotations

# JSON is used to load preprocessing metadata.
import json
# `Path` provides convenient file access for metadata loading.
from pathlib import Path
# `Any` is used for flexible dictionary-like raw input payloads.
from typing import Any

# NumPy is used to find the winning class and shape the result.
import numpy as np
# Torch loads the checkpoint and runs the recurrent model.
import torch

# Import the default checkpoint and metadata paths.
from config import CHECKPOINT_FILE, PREPROCESSING_METADATA_FILE
# Import the shared event-to-feature encoder.
from features import event_to_feature_vector
# Import the GRU classifier.
from model import BehaviorGRU
# Import the typed event schema.
from schemas import RawEvent


class StreamBehaviorPredictor:
    """Stateful predictor that scores one event at a time."""

    def __init__(
        self,
        model_path: str = str(CHECKPOINT_FILE),
        metadata_path: str = str(PREPROCESSING_METADATA_FILE),
        device: str = "cpu",
    ) -> None:
        """Load the trained model and the preprocessing metadata."""

        # Resolve the requested execution device.
        self.device = torch.device(device)
        # Load the metadata so streaming inference can exactly match training.
        self.metadata = json.loads(Path(metadata_path).read_text(encoding="utf-8"))
        # Load the saved checkpoint from disk.
        checkpoint = torch.load(model_path, map_location=self.device)

        # Rebuild the model with the saved dimensions.
        self.model = BehaviorGRU(
            input_size=checkpoint["feature_dim"],
            hidden_size=checkpoint["hidden_size"],
            num_classes=checkpoint["num_classes"],
        ).to(self.device)
        # Load the trained weights.
        self.model.load_state_dict(checkpoint["model_state_dict"])
        # Switch the model into inference mode.
        self.model.eval()

        # Convert the label map from metadata into an index-to-label dictionary.
        self.id_to_label = {int(index): label for label, index in self.metadata["labels"].items()}
        # Hold the recurrent hidden state between events.
        self.hidden: torch.Tensor | None = None
        # Track the timestamp of the last processed event.
        self.last_timestamp_ms: int | None = None
        # Store the inactivity threshold used to reset a session.
        self.session_idle_reset_ms = int(self.metadata["session_idle_reset_ms"])
        # Store the feature dimension for reshape operations.
        self.feature_dim = int(self.metadata["feature_dim"])

    def reset(self) -> None:
        """Reset streaming state when a session ends or becomes stale."""

        self.hidden = None
        self.last_timestamp_ms = None

    def _maybe_reset_for_gap(self, event: RawEvent) -> None:
        """Reset the recurrent state if the inactivity gap is too large."""

        # If this is the first event, there is no previous gap to inspect.
        if self.last_timestamp_ms is None:
            return
        # If the gap exceeds the configured threshold, treat it as a new session.
        if event.timestamp_ms - self.last_timestamp_ms > self.session_idle_reset_ms:
            self.reset()

    def predict_event(self, raw_event: RawEvent | dict[str, Any]) -> dict[str, Any]:
        """Predict behavior from one new event and update hidden state."""

        # Accept either a `RawEvent` instance or a plain dictionary payload.
        event = raw_event if isinstance(raw_event, RawEvent) else RawEvent.from_dict(raw_event)
        # Reset the recurrent state if the event arrives after a long gap.
        self._maybe_reset_for_gap(event)

        # Encode the raw event exactly the same way preprocessing did.
        feature_vector = event_to_feature_vector(event, self.last_timestamp_ms)
        # Reshape the feature vector into `[batch=1, seq_len=1, feature_dim]`.
        x = torch.tensor(feature_vector, dtype=torch.float32, device=self.device).view(1, 1, self.feature_dim)

        # Turn off gradient tracking because this is inference only.
        with torch.no_grad():
            # Feed the single event plus the previous hidden state into the GRU.
            logits, self.hidden = self.model(x, self.hidden)
            # Convert logits into class probabilities.
            probabilities = torch.softmax(logits, dim=1)[0].cpu().numpy()

        # Remember the timestamp so the next event can compute a time delta.
        self.last_timestamp_ms = event.timestamp_ms
        # Select the most probable class id.
        predicted_id = int(np.argmax(probabilities))
        # Return a readable result payload.
        return {
            "label": self.id_to_label[predicted_id],
            "confidence": float(probabilities[predicted_id]),
            "scores": {
                self.id_to_label[index]: float(score)
                for index, score in enumerate(probabilities.tolist())
            },
        }


def main() -> None:
    """Run a tiny demo of streaming inference with a richer multi-event session."""

    # Build the predictor using default checkpoint and metadata paths.
    predictor = StreamBehaviorPredictor()
    # Create a short demo session that resembles a comparing-style browsing
    # pattern: moderate scrolling, a reversal, then text selection and a
    # deliberate click after some dwell time.
    demo_events = [
        {
            "session_id": "demo_comparing",
            "timestamp_ms": 1_000,
            "event_type": "scroll",
            "x": 0.0,
            "y": 220.0,
            "delta_y": 180.0,
            "velocity": 720.0,
            "acceleration": 110.0,
            "direction": 1,
            "pressure": 0.0,
            "duration_ms": 0.0,
            "dwell_before_ms": 0.0,
            "selection_word_count": 0.0,
            "label": "comparing",
        },
        {
            "session_id": "demo_comparing",
            "timestamp_ms": 1_240,
            "event_type": "scroll",
            "x": 0.0,
            "y": 410.0,
            "delta_y": 165.0,
            "velocity": 680.0,
            "acceleration": -140.0,
            "direction": -1,
            "pressure": 0.0,
            "duration_ms": 0.0,
            "dwell_before_ms": 0.0,
            "selection_word_count": 0.0,
            "label": "comparing",
        },
        {
            "session_id": "demo_comparing",
            "timestamp_ms": 1_620,
            "event_type": "selection",
            "x": 188.0,
            "y": 640.0,
            "delta_y": 0.0,
            "velocity": 0.0,
            "acceleration": 0.0,
            "direction": 0,
            "pressure": 0.0,
            "duration_ms": 1800.0,
            "dwell_before_ms": 0.0,
            "selection_word_count": 14.0,
            "label": "comparing",
        },
        {
            "session_id": "demo_comparing",
            "timestamp_ms": 2_050,
            "event_type": "click",
            "x": 205.0,
            "y": 670.0,
            "delta_y": 0.0,
            "velocity": 0.0,
            "acceleration": 0.0,
            "direction": 0,
            "pressure": 0.0,
            "duration_ms": 0.0,
            "dwell_before_ms": 3200.0,
            "selection_word_count": 0.0,
            "label": "comparing",
        },
    ]

    # Score each event sequentially and print the updated prediction.
    for payload in demo_events:
        print(predictor.predict_event(payload))


if __name__ == "__main__":
    main()

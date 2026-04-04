"""Offline preprocessing pipeline.

This module converts raw JSONL event sessions into fixed-length model inputs and
produces the train/validation/test splits consumed by the training script.
"""

# Postpone annotation evaluation for cleaner type hints.
from __future__ import annotations

# JSON is used to read raw events and write preprocessing metadata.
import json
# `defaultdict` makes it easy to group events by session id.
from collections import defaultdict

# NumPy stores the processed arrays on disk.
import numpy as np
# Scikit-learn provides a convenient stratified split helper.
from sklearn.model_selection import train_test_split

# Import all preprocessing-related paths and constants from one place.
from config import (
    LABEL_TO_ID,
    MIN_WINDOW_EVENTS,
    PREPROCESSING_METADATA_FILE,
    PROCESSED_DATA_DIR,
    RAW_EVENTS_FILE,
    SEED,
    TEST_DATA_FILE,
    TRAIN_DATA_FILE,
    VAL_DATA_FILE,
    WINDOW_STRIDE,
)
# Import the shared feature encoding logic so preprocessing and inference match.
from features import build_preprocessing_metadata, event_to_feature_vector, pad_or_truncate
# Import the structured event schema used while parsing raw payloads.
from schemas import RawEvent


def load_sessions() -> dict[str, list[RawEvent]]:
    """Read the raw JSONL file and group events by session id."""

    # Create an empty list for a session the first time we see its id.
    sessions: dict[str, list[RawEvent]] = defaultdict(list)
    # Open the raw events file for reading.
    with RAW_EVENTS_FILE.open(encoding="utf-8") as handle:
        # Iterate through each line in the JSONL file.
        for line in handle:
            # Skip accidental blank lines.
            if not line.strip():
                continue
            # Parse the JSON and convert it into a typed `RawEvent`.
            event = RawEvent.from_dict(json.loads(line))
            # Append the event to its session bucket.
            sessions[event.session_id].append(event)

    # Make sure every session is ordered chronologically before feature encoding.
    for session_events in sessions.values():
        session_events.sort(key=lambda event: event.timestamp_ms)
    # Return the grouped and sorted session dictionary.
    return sessions


def split_session_ids(session_labels: dict[str, int]) -> tuple[list[str], list[str], list[str]]:
    """Split sessions into train, validation, and test sets.

    Splitting by session prevents leakage where events from the same session end
    up in both training and evaluation splits.
    """

    # Extract the session ids into a list.
    session_ids = list(session_labels)
    # Build a parallel label list for stratified splitting.
    labels = [session_labels[session_id] for session_id in session_ids]

    # First split into train and a temporary holdout set.
    train_ids, temp_ids, _, temp_labels = train_test_split(
        session_ids,
        labels,
        test_size=0.30,
        random_state=SEED,
        stratify=labels,
    )
    # Then split the holdout set evenly into validation and test.
    val_ids, test_ids = train_test_split(
        temp_ids,
        test_size=0.50,
        random_state=SEED,
        stratify=temp_labels,
    )
    # Return the three split lists.
    return train_ids, val_ids, test_ids


def build_windows(sessions: dict[str, list[RawEvent]], session_ids: list[str]) -> tuple[np.ndarray, np.ndarray]:
    """Build fixed-length training samples from variable-length sessions."""

    # This list will collect every encoded sample window.
    features: list[list[list[float]]] = []
    # This list will collect the matching class id for each sample window.
    labels: list[int] = []

    # Process one session at a time.
    for session_id in session_ids:
        # Retrieve the chronologically sorted event list for this session.
        events = sessions[session_id]
        # The current synthetic dataset uses the session's final label as the
        # label for the full sequence and all prefix windows derived from it.
        label_id = LABEL_TO_ID[events[-1].label]

        # Store the encoded event vectors for the current session.
        encoded_sequence: list[list[float]] = []
        # We need the previous timestamp to compute `time_delta_norm`.
        prev_timestamp_ms: int | None = None
        # Encode each raw event into the shared feature format.
        for event in events:
            encoded_sequence.append(event_to_feature_vector(event, prev_timestamp_ms))
            prev_timestamp_ms = event.timestamp_ms

        # Create multiple prefix windows so the model can learn from both early
        # and late portions of a session, not only the very end.
        candidate_end_indices = list(range(MIN_WINDOW_EVENTS, len(encoded_sequence) + 1, WINDOW_STRIDE))
        # Always ensure the full session is included as a training example.
        if not candidate_end_indices or candidate_end_indices[-1] != len(encoded_sequence):
            candidate_end_indices.append(len(encoded_sequence))

        # Materialize each prefix window into a fixed `[SEQ_LEN, FEATURE_DIM]`
        # sample using padding or truncation.
        for end_index in candidate_end_indices:
            features.append(pad_or_truncate(encoded_sequence[:end_index]))
            labels.append(label_id)

    # Convert the Python lists into NumPy arrays ready for disk storage.
    return np.asarray(features, dtype=np.float32), np.asarray(labels, dtype=np.int64)


def save_split(path, X: np.ndarray, y: np.ndarray) -> None:
    """Save one processed split to disk."""

    np.savez(path, X=X, y=y)


def main() -> None:
    """Run the full preprocessing pipeline from raw JSONL to saved splits."""

    # Ensure the processed data directory exists.
    PROCESSED_DATA_DIR.mkdir(parents=True, exist_ok=True)
    # Ensure the metadata directory exists.
    PREPROCESSING_METADATA_FILE.parent.mkdir(parents=True, exist_ok=True)

    # Load and group the raw sessions.
    sessions = load_sessions()
    # Build a per-session label map used for stratified splitting.
    session_labels = {session_id: LABEL_TO_ID[events[-1].label] for session_id, events in sessions.items()}
    # Split sessions into train, validation, and test buckets.
    train_ids, val_ids, test_ids = split_session_ids(session_labels)

    # Build windows for the training split.
    X_train, y_train = build_windows(sessions, train_ids)
    # Build windows for the validation split.
    X_val, y_val = build_windows(sessions, val_ids)
    # Build windows for the test split.
    X_test, y_test = build_windows(sessions, test_ids)

    # Save the train split.
    save_split(TRAIN_DATA_FILE, X_train, y_train)
    # Save the validation split.
    save_split(VAL_DATA_FILE, X_val, y_val)
    # Save the test split.
    save_split(TEST_DATA_FILE, X_test, y_test)

    # Start with the core metadata shared across train and inference.
    metadata = build_preprocessing_metadata()
    # Add summary statistics that are useful for debugging and documentation.
    metadata.update(
        {
            "train_sessions": len(train_ids),
            "val_sessions": len(val_ids),
            "test_sessions": len(test_ids),
            "train_samples": int(len(X_train)),
            "val_samples": int(len(X_val)),
            "test_samples": int(len(X_test)),
        }
    )
    # Write the metadata JSON to disk.
    PREPROCESSING_METADATA_FILE.write_text(json.dumps(metadata, indent=2), encoding="utf-8")

    # Print summary shapes so the user can verify preprocessing worked.
    print(f"train: {X_train.shape} {y_train.shape}")
    print(f"val:   {X_val.shape} {y_val.shape}")
    print(f"test:  {X_test.shape} {y_test.shape}")
    print(f"metadata: {PREPROCESSING_METADATA_FILE}")


if __name__ == "__main__":
    main()

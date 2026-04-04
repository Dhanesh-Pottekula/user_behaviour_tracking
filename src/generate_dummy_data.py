"""Generate synthetic behavior sessions for the end-to-end pipeline.

The goal of this file is not to simulate perfect real-world telemetry. Instead,
it creates synthetic sessions with distinct class-specific patterns so the whole
training and inference pipeline can be developed and tested before real data is
available.
"""

# Enable postponed evaluation of annotations.
from __future__ import annotations

# JSON is used to write one event per line to the raw data file.
import json
# `random` drives all synthetic behavior sampling.
import random
# `Counter` is used only for summary statistics after generation.
from collections import Counter

# Import label vocabulary, output paths, screen dimensions, and seed values.
from config import BEHAVIOR_LABELS, RAW_DATA_DIR, RAW_EVENTS_FILE, SCREEN_HEIGHT, SCREEN_WIDTH, SEED
# Import the structured raw event schema.
from schemas import RawEvent


def bounded(value: float, low: float, high: float) -> float:
    """Clamp a value to the inclusive range `[low, high]`."""

    return max(low, min(high, value))


def make_scroll_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str, *, fast: bool, direction: int) -> RawEvent:
    """Create one synthetic scroll event."""

    velocity = rng.uniform(900.0, 2200.0) if fast else rng.uniform(120.0, 900.0)
    delta_y = rng.uniform(150.0, 700.0) if fast else rng.uniform(25.0, 220.0)
    acceleration = rng.uniform(-900.0, 900.0) if fast else rng.uniform(-250.0, 250.0)
    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="scroll",
        x=0.0,
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        delta_y=delta_y,
        velocity=velocity,
        acceleration=acceleration,
        direction=direction,
        label=label,
    )


def make_click_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str, *, frustrated: bool = False) -> RawEvent:
    """Create one synthetic click event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="click",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        dwell_before_ms=rng.uniform(50.0, 500.0) if frustrated else rng.uniform(400.0, 2400.0),
        label=label,
    )


def make_deliberate_click_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str) -> RawEvent:
    """Create a click event that suggests careful consideration before acting."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="click",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        dwell_before_ms=rng.uniform(1500.0, 6000.0),
        label=label,
    )


def make_touch_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str, *, pressured: bool = False) -> RawEvent:
    """Create one synthetic touch event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="touch",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        pressure=rng.uniform(0.6, 1.0) if pressured else rng.uniform(0.05, 0.65),
        duration_ms=rng.uniform(30.0, 220.0) if pressured else rng.uniform(120.0, 900.0),
        label=label,
    )


def make_selection_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str) -> RawEvent:
    """Create one synthetic text-selection event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="selection",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        duration_ms=rng.uniform(300.0, 1800.0),
        selection_word_count=rng.uniform(3.0, 22.0),
        label=label,
    )


def make_idle_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str, *, long_idle: bool) -> RawEvent:
    """Create one synthetic idle event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="idle",
        duration_ms=rng.uniform(2500.0, 12000.0) if long_idle else rng.uniform(600.0, 3000.0),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        label=label,
    )


def make_navigation_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str) -> RawEvent:
    """Create one synthetic navigation event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="navigation",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        dwell_before_ms=rng.uniform(600.0, 2600.0),
        label=label,
    )


def make_error_event(rng: random.Random, session_id: str, timestamp_ms: int, label: str) -> RawEvent:
    """Create one synthetic error-style event."""

    return RawEvent(
        session_id=session_id,
        timestamp_ms=timestamp_ms,
        event_type="error",
        x=rng.uniform(0.0, SCREEN_WIDTH),
        y=rng.uniform(0.0, SCREEN_HEIGHT),
        duration_ms=rng.uniform(40.0, 250.0),
        label=label,
    )


def next_timestamp(rng: random.Random, label: str) -> int:
    """Sample the next inter-event delay based on the target behavior label."""

    if label == "ignore":
        return rng.randint(900, 3500)
    if label == "skimming":
        return rng.randint(40, 180)
    if label == "frustrated":
        return rng.randint(20, 140)
    if label == "hunting":
        return rng.randint(120, 550)
    if label == "engaged":
        return rng.randint(80, 240)
    if label == "confused":
        return rng.randint(220, 900)
    if label == "comparing":
        return rng.randint(120, 380)
    if label == "deep_reading":
        return rng.randint(400, 1500)
    return rng.randint(100, 450)


def build_behavior_session(rng: random.Random, session_id: str, label: str) -> list[RawEvent]:
    """Generate one full session for a chosen behavior class."""

    # Randomize the session length so the model sees variable-length journeys.
    if label == "deep_reading":
        event_count = rng.randint(30, 55)
    elif label == "ignore":
        event_count = rng.randint(25, 50)
    else:
        event_count = rng.randint(40, 90)
    # Start from an arbitrary base timestamp.
    timestamp_ms = 1_000_000
    # Collect the generated events in order.
    events: list[RawEvent] = []
    # Track scroll direction for the frustrated pattern where reversals matter.
    scroll_direction = 1

    for _ in range(event_count):
        # Advance time according to the current class pattern.
        timestamp_ms += next_timestamp(rng, label)
        # Add small random perturbations in a minority of events.
        noise = rng.random() < 0.08

        if label == "skimming":
            # Skimming should look like fast, frequent scrolling with only a few
            # interruptions.
            choice = rng.choices(["scroll", "touch", "click", "idle"], weights=[0.72, 0.15, 0.08, 0.05], k=1)[0]
            if choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=True, direction=1))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label))
            elif choice == "click":
                events.append(make_click_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
        elif label == "hunting":
            # Hunting mixes browsing with more deliberate actions such as
            # clicking, navigating, and making selections.
            choice = rng.choices(
                ["scroll", "click", "selection", "navigation", "idle"],
                weights=[0.34, 0.25, 0.16, 0.15, 0.10],
                k=1,
            )[0]
            if choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=1))
            elif choice == "click":
                events.append(make_click_event(rng, session_id, timestamp_ms, label))
            elif choice == "selection":
                events.append(make_selection_event(rng, session_id, timestamp_ms, label))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
        elif label == "normal":
            # Normal behavior is a more balanced mixture of common actions.
            choice = rng.choices(
                ["scroll", "click", "touch", "idle", "navigation"],
                weights=[0.42, 0.20, 0.20, 0.10, 0.08],
                k=1,
            )[0]
            if choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=1))
            elif choice == "click":
                events.append(make_click_event(rng, session_id, timestamp_ms, label))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
        elif label == "ignore":
            # Ignore sessions spend more time idle and generally interact less.
            choice = rng.choices(["idle", "scroll", "touch", "navigation"], weights=[0.55, 0.25, 0.12, 0.08], k=1)[0]
            if choice == "idle":
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=True))
            elif choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=1))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
        elif label == "engaged":
            # Engaged sessions are active, varied, and purposeful without looking
            # rushed or erratic.
            choice = rng.choices(
                ["scroll", "click", "touch", "selection", "navigation", "idle"],
                weights=[0.28, 0.20, 0.16, 0.16, 0.12, 0.08],
                k=1,
            )[0]
            if choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=1))
            elif choice == "click":
                events.append(make_click_event(rng, session_id, timestamp_ms, label))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label))
            elif choice == "selection":
                events.append(make_selection_event(rng, session_id, timestamp_ms, label))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
        elif label == "confused":
            # Confused sessions show hesitation, retries, and erratic task
            # switching without the extreme speed of frustration.
            choice = rng.choices(
                ["scroll", "click", "touch", "navigation", "idle", "error"],
                weights=[0.24, 0.18, 0.12, 0.18, 0.18, 0.10],
                k=1,
            )[0]
            if choice == "scroll":
                scroll_direction *= -1 if rng.random() < 0.45 else 1
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=scroll_direction))
            elif choice == "click":
                events.append(make_deliberate_click_event(rng, session_id, timestamp_ms, label))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            elif choice == "idle":
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
            else:
                events.append(make_error_event(rng, session_id, timestamp_ms, label))
        elif label == "comparing":
            # Comparing sessions bounce between nearby items with repeated scroll
            # reversals, deliberate clicks, and moderate reading pauses.
            choice = rng.choices(
                ["scroll", "click", "selection", "navigation", "idle"],
                weights=[0.42, 0.18, 0.18, 0.12, 0.10],
                k=1,
            )[0]
            if choice == "scroll":
                scroll_direction *= -1 if rng.random() < 0.55 else 1
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=scroll_direction))
            elif choice == "click":
                events.append(make_deliberate_click_event(rng, session_id, timestamp_ms, label))
            elif choice == "selection":
                events.append(make_selection_event(rng, session_id, timestamp_ms, label))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
        elif label == "deep_reading":
            # Deep reading favors slow progress, long dwell times, selections,
            # and relatively little abrupt movement.
            choice = rng.choices(
                ["scroll", "selection", "idle", "touch", "click"],
                weights=[0.30, 0.24, 0.22, 0.14, 0.10],
                k=1,
            )[0]
            if choice == "scroll":
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=False, direction=1))
            elif choice == "selection":
                selection_event = make_selection_event(rng, session_id, timestamp_ms, label)
                selection_event.duration_ms = rng.uniform(1200.0, 4200.0)
                selection_event.selection_word_count = rng.uniform(8.0, 45.0)
                events.append(selection_event)
            elif choice == "idle":
                events.append(make_idle_event(rng, session_id, timestamp_ms, label, long_idle=False))
            elif choice == "touch":
                touch_event = make_touch_event(rng, session_id, timestamp_ms, label)
                touch_event.duration_ms = rng.uniform(500.0, 2500.0)
                events.append(touch_event)
            else:
                events.append(make_deliberate_click_event(rng, session_id, timestamp_ms, label))
        else:
            # Frustrated sessions include faster scrolls, more reversals, and
            # more forceful or error-like interactions.
            choice = rng.choices(
                ["scroll", "click", "touch", "error", "navigation"],
                weights=[0.45, 0.20, 0.15, 0.12, 0.08],
                k=1,
            )[0]
            if choice == "scroll":
                # Reverse direction more often than other classes.
                scroll_direction *= -1 if rng.random() < 0.6 else 1
                events.append(make_scroll_event(rng, session_id, timestamp_ms, label, fast=True, direction=scroll_direction))
            elif choice == "click":
                events.append(make_click_event(rng, session_id, timestamp_ms, label, frustrated=True))
            elif choice == "touch":
                events.append(make_touch_event(rng, session_id, timestamp_ms, label, pressured=True))
            elif choice == "navigation":
                events.append(make_navigation_event(rng, session_id, timestamp_ms, label))
            else:
                events.append(make_error_event(rng, session_id, timestamp_ms, label))

        if noise:
            # Jitter a small number of spatial coordinates so the synthetic data
            # is not unrealistically clean.
            events[-1].x = bounded(events[-1].x + rng.uniform(-20.0, 20.0), 0.0, SCREEN_WIDTH)
            events[-1].y = bounded(events[-1].y + rng.uniform(-80.0, 80.0), 0.0, SCREEN_HEIGHT)

    # Return the full event sequence for this synthetic session.
    return events


def main() -> None:
    """Generate the full synthetic raw dataset and write it to disk."""

    # Use a fixed seed so generation is reproducible.
    rng = random.Random(SEED)
    # Ensure the raw data directory exists before writing.
    RAW_DATA_DIR.mkdir(parents=True, exist_ok=True)

    # Create the same number of sessions per class for a balanced dataset.
    sessions_per_label = 120
    # Keep counts for a readable console summary.
    counts: Counter[str] = Counter()

    # Open the JSONL file for writing.
    with RAW_EVENTS_FILE.open("w", encoding="utf-8") as handle:
        # Iterate over every supported behavior label.
        for label in BEHAVIOR_LABELS:
            # Generate multiple sessions for that label.
            for session_index in range(sessions_per_label):
                # Create a human-readable synthetic session id.
                session_id = f"{label}_session_{session_index:04d}"
                # Generate the full list of events for this synthetic session.
                for event in build_behavior_session(rng, session_id, label):
                    # Count the event for summary reporting.
                    counts[label] += 1
                    # Write one JSON object per line.
                    handle.write(json.dumps(event.to_dict()) + "\n")

    # Print a summary so the user can verify that generation completed.
    print(f"Wrote {sum(counts.values())} events to {RAW_EVENTS_FILE}")
    # Print per-label event totals for quick sanity checking.
    for label in BEHAVIOR_LABELS:
        print(f"{label:12s}: {counts[label]}")


if __name__ == "__main__":
    main()

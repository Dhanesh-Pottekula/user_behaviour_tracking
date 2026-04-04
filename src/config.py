"""Central configuration for the user behavior tracker project.

This file intentionally collects every global constant in one place so the rest
of the codebase can import from here instead of repeating values in multiple
modules. That makes the training pipeline, streaming inference path, and ONNX
export path stay aligned.
"""

# `Path` is used to build filesystem paths in a platform-safe way.
from pathlib import Path

# Resolve the absolute project root from the location of this file.
PROJECT_ROOT = Path(__file__).resolve().parent.parent

# Define the top-level data directory.
DATA_DIR = PROJECT_ROOT / "data"
# Raw JSONL event logs live here.
RAW_DATA_DIR = DATA_DIR / "raw"
# Preprocessed NumPy training splits live here.
PROCESSED_DATA_DIR = DATA_DIR / "processed"
# All generated model outputs live here.
OUTPUTS_DIR = PROJECT_ROOT / "outputs"
# Best PyTorch checkpoints are written here.
CHECKPOINT_DIR = OUTPUTS_DIR / "checkpoints"
# Exported ONNX models are written here.
ONNX_DIR = OUTPUTS_DIR / "onnx"
# Metadata that must be shared with inference is written here.
METADATA_DIR = OUTPUTS_DIR / "metadata"

# Single raw JSONL file used by the current synthetic-data pipeline.
RAW_EVENTS_FILE = RAW_DATA_DIR / "events.jsonl"
# Training split saved by preprocessing.
TRAIN_DATA_FILE = PROCESSED_DATA_DIR / "train.npz"
# Validation split saved by preprocessing.
VAL_DATA_FILE = PROCESSED_DATA_DIR / "val.npz"
# Test split saved by preprocessing.
TEST_DATA_FILE = PROCESSED_DATA_DIR / "test.npz"
# Metadata file that records feature order, labels, normalization, and shapes.
PREPROCESSING_METADATA_FILE = METADATA_DIR / "preprocessing.json"
# Best model checkpoint selected during training.
CHECKPOINT_FILE = CHECKPOINT_DIR / "best_model.pt"
# Exported ONNX model path.
ONNX_FILE = ONNX_DIR / "behavior_gru.onnx"

# Fixed random seed used across generation, splitting, and training.
SEED = 42
# Number of time steps in every offline training sample.
SEQ_LEN = 50
# Step size used when creating multiple windows from one session.
WINDOW_STRIDE = 8
# Minimum number of events required before we start emitting training windows.
MIN_WINDOW_EVENTS = 8
# Number of samples per optimizer step.
BATCH_SIZE = 32
# Number of full passes over the training dataset.
EPOCHS = 16
# Optimizer learning rate.
LEARNING_RATE = 1e-3
# Weight decay for AdamW regularization.
WEIGHT_DECAY = 1e-4
# Size of the GRU hidden state.
HIDDEN_SIZE = 48
# Number of stacked GRU layers.
NUM_GRU_LAYERS = 1

# Approximate UI width used to normalize x coordinates.
SCREEN_WIDTH = 400.0
# Approximate UI height used to normalize y coordinates.
SCREEN_HEIGHT = 1200.0
# If the gap between two events is bigger than this threshold, streaming
# inference treats it as a fresh interaction and resets hidden state.
SESSION_IDLE_RESET_MS = 30_000

# Vocabulary of supported low-level event types.
EVENT_TYPES = (
    "scroll",
    "click",
    "touch",
    "selection",
    "idle",
    "error",
    "navigation",
)
# Integer ids are still useful for metadata and debugging, even though the
# actual model input uses one-hot encoding instead of raw ids.
EVENT_TYPE_TO_ID = {name: index for index, name in enumerate(EVENT_TYPES)}

# Vocabulary of behavior classes the model predicts.
BEHAVIOR_LABELS = (
    "skimming",
    "hunting",
    "normal",
    "ignore",
    "frustrated",
    "engaged",
    "confused",
    "comparing",
    "deep_reading",
)
# Mapping from label string to class index.
LABEL_TO_ID = {label: index for index, label in enumerate(BEHAVIOR_LABELS)}
# Reverse mapping from class index back to label string.
ID_TO_LABEL = {index: label for label, index in LABEL_TO_ID.items()}
# Total number of output classes.
NUM_CLASSES = len(BEHAVIOR_LABELS)

# Feature names for the event-type one-hot portion of the model input.
EVENT_TYPE_FEATURES = [f"event_type_{name}" for name in EVENT_TYPES]
# Feature names for the normalized continuous portion of the model input.
CONTINUOUS_FEATURES = [
    "velocity_norm",
    "acceleration_norm",
    "direction_norm",
    "delta_y_norm",
    "x_norm",
    "y_norm",
    "pressure_norm",
    "duration_norm",
    "dwell_before_norm",
    "selection_word_count_norm",
    "time_delta_norm",
]
# Full feature order used everywhere in preprocessing and inference.
FEATURE_NAMES = EVENT_TYPE_FEATURES + CONTINUOUS_FEATURES
# Final size of one encoded event vector.
FEATURE_DIM = len(FEATURE_NAMES)

# Per-field scaling values used to normalize raw event attributes into ranges
# that are easier for the model to learn from.
NORMALIZATION_LIMITS = {
    "velocity": 2500.0,
    "acceleration": 1200.0,
    "delta_y": 4000.0,
    "duration_ms": 10_000.0,
    "dwell_before_ms": 15_000.0,
    "selection_word_count": 100.0,
    "time_delta_ms": 15_000.0,
}

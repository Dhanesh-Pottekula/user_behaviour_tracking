# User Behavior Tracker

A GRU-based streaming behavior classifier built with PyTorch, ONNX, and ONNX Runtime.

This project is designed for two modes:

- Offline training on fixed-length event sequences.
- Online streaming inference that consumes one event at a time and carries the GRU hidden state forward.

## What The Project Does

The pipeline models user behavior from low-level interaction events such as:

- `scroll`
- `click`
- `touch`
- `selection`
- `idle`
- `error`
- `navigation`

It predicts one of these behavior classes:

- `skimming`
- `hunting`
- `normal`
- `ignore`
- `frustrated`
- `engaged`
- `confused`
- `comparing`
- `deep_reading`

## Project Structure

```text
user-behavior-tracker/
  data/
    raw/
    processed/
  outputs/
    checkpoints/
    metadata/
    onnx/
  src/
    config.py
    schemas.py
    features.py
    generate_dummy_data.py
    preprocess.py
    dataset.py
    model.py
    train.py
    evaluate.py
    stream_inference.py
    export_onnx.py
    test_onnx.py
  README.md
  ARCHITECTURE.md
```

## Main Files

- [src/config.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/config.py): global configuration, labels, feature names, paths, and hyperparameters
- [src/schemas.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/schemas.py): raw event dataclass
- [src/features.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/features.py): feature encoding and normalization
- [src/generate_dummy_data.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/generate_dummy_data.py): synthetic training-data generator
- [src/preprocess.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/preprocess.py): session grouping, encoding, windowing, and train/val/test split generation
- [src/model.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/model.py): GRU classifier
- [src/train.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/train.py): training loop and checkpoint saving
- [src/evaluate.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/evaluate.py): test-set evaluation
- [src/stream_inference.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/stream_inference.py): one-event-at-a-time inference with hidden-state carryover
- [src/export_onnx.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/export_onnx.py): ONNX export
- [src/test_onnx.py](/Users/dhanesh/Desktop/p/user-behavior-tracker/src/test_onnx.py): ONNX parity testing

## End-To-End Flow

1. Generate synthetic raw sessions.
2. Preprocess raw sessions into fixed-length model inputs.
3. Train the GRU classifier.
4. Evaluate the checkpoint on the test split.
5. Run streaming inference event by event.
6. Export the model to ONNX.
7. Compare ONNX Runtime outputs with PyTorch outputs.

## Quickstart

Run the project with the local virtual environment:

```bash
./.venv/bin/python src/generate_dummy_data.py
./.venv/bin/python src/preprocess.py
./.venv/bin/python src/train.py
./.venv/bin/python src/evaluate.py
./.venv/bin/python src/stream_inference.py
./.venv/bin/python src/export_onnx.py
./.venv/bin/python src/test_onnx.py
```

## Training Outputs

After preprocessing, these files are created:

- `data/processed/train.npz`
- `data/processed/val.npz`
- `data/processed/test.npz`
- `outputs/metadata/preprocessing.json`

After training, this file is created:

- `outputs/checkpoints/best_model.pt`

After export, this file is created:

- `outputs/onnx/behavior_gru.onnx`

## Input And Output Shapes

- Encoded event feature vector: `18`
- Training sample shape: `[50, 18]`
- Training batch shape: `[batch, 50, 18]`
- Streaming input shape: `[1, 1, 18]`
- Hidden state shape: `[1, batch, 48]`
- Output logits shape: `[batch, 9]`

## Streaming Inference Concept

The offline model is trained on fixed-length sequences, but the runtime path uses the same GRU one event at a time:

1. Read a new event.
2. Encode it into a feature vector.
3. Reshape to `[1, 1, feature_dim]`.
4. Pass it into the GRU with the previous hidden state.
5. Get new logits and updated hidden state.
6. Keep the hidden state for the next event.
7. Reset the hidden state when the session ends or when the inactivity gap is too large.

## Architecture Reference

Detailed architecture documentation is available in [ARCHITECTURE.md](/Users/dhanesh/Desktop/p/user-behavior-tracker/ARCHITECTURE.md).

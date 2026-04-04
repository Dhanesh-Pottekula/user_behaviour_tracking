# User Behavior Tracker

A GRU-based streaming behavior classifier built with PyTorch.

The project supports:

- Offline training on fixed-length event sequences.
- Online inference that processes one event at a time while carrying the GRU hidden state forward.

## Quickstart

```bash
./.venv/bin/python src/generate_dummy_data.py
./.venv/bin/python src/preprocess.py
./.venv/bin/python src/train.py
./.venv/bin/python src/evaluate.py
./.venv/bin/python src/export_onnx.py
./.venv/bin/python src/test_onnx.py
```

"""Validate that ONNX Runtime matches PyTorch numerically."""

# Enable postponed evaluation of type annotations.
from __future__ import annotations

# NumPy builds deterministic test inputs and compares outputs.
import numpy as np
# ONNX Runtime executes the exported ONNX graph.
import onnxruntime as ort
# Torch loads the checkpoint and runs the reference PyTorch model.
import torch

# Import file paths for the checkpoint and exported ONNX model.
from config import CHECKPOINT_FILE, ONNX_FILE
# Import the reference GRU implementation.
from model import BehaviorGRU


def compare_arrays(name: str, left: np.ndarray, right: np.ndarray, tolerance: float = 1e-4) -> None:
    """Compare two arrays and fail if they differ beyond tolerance."""

    # Compute the largest absolute difference between the two outputs.
    max_abs_diff = float(np.max(np.abs(left - right)))
    # Print the difference for visibility during validation.
    print(f"{name} max_abs_diff={max_abs_diff:.6f}")
    # Raise an error if the difference is too large.
    if max_abs_diff > tolerance:
        raise AssertionError(f"{name} differs by {max_abs_diff:.6f}, above tolerance {tolerance}")


def main() -> None:
    """Run both full-sequence and streaming parity checks."""

    # Load the trained checkpoint on CPU.
    checkpoint = torch.load(CHECKPOINT_FILE, map_location="cpu")

    # Recreate the PyTorch model using the saved dimensions.
    model = BehaviorGRU(
        input_size=checkpoint["feature_dim"],
        hidden_size=checkpoint["hidden_size"],
        num_classes=checkpoint["num_classes"],
    )
    # Load the learned parameters.
    model.load_state_dict(checkpoint["model_state_dict"])
    # Put the model in evaluation mode.
    model.eval()

    # Open the exported ONNX model with the CPU execution provider.
    ort_session = ort.InferenceSession(str(ONNX_FILE), providers=["CPUExecutionProvider"])

    # Create a deterministic random number generator for repeatable test inputs.
    rng = np.random.default_rng(1234)
    # Generate one random event sequence.
    sequence = rng.normal(size=(1, 9, checkpoint["feature_dim"])).astype(np.float32)
    # Create a zero initial hidden state.
    h0 = np.zeros((model.num_layers, 1, checkpoint["hidden_size"]), dtype=np.float32)

    # Run the reference PyTorch model on the full sequence.
    with torch.no_grad():
        torch_logits, torch_hn = model(torch.from_numpy(sequence), torch.from_numpy(h0))

    # Run the ONNX model on the full sequence.
    ort_logits, ort_hn = ort_session.run(None, {"input": sequence, "h0": h0})
    # Compare full-sequence logits.
    compare_arrays("batched_logits", torch_logits.numpy(), np.asarray(ort_logits))
    # Compare full-sequence final hidden states.
    compare_arrays("batched_hidden", torch_hn.numpy(), np.asarray(ort_hn))

    # Initialize the PyTorch hidden state for streaming-style stepwise testing.
    streaming_torch_hidden = torch.from_numpy(h0.copy())
    # Initialize the ONNX hidden state for streaming-style stepwise testing.
    streaming_onnx_hidden = h0.copy()
    # Feed the same sequence one event at a time through both systems.
    for step_index in range(sequence.shape[1]):
        # Slice one time step while preserving batch and sequence dimensions.
        step = sequence[:, step_index : step_index + 1, :]
        # Run the PyTorch model on the single-step input and carried hidden state.
        with torch.no_grad():
            torch_step_logits, streaming_torch_hidden = model(torch.from_numpy(step), streaming_torch_hidden)
        # Run the ONNX model on the same step and hidden state.
        ort_step_logits, ort_step_hidden = ort_session.run(None, {"input": step, "h0": streaming_onnx_hidden})
        # Compare single-step logits.
        compare_arrays(f"stream_step_{step_index}_logits", torch_step_logits.numpy(), np.asarray(ort_step_logits))
        # Compare single-step hidden states.
        compare_arrays(f"stream_step_{step_index}_hidden", streaming_torch_hidden.numpy(), np.asarray(ort_step_hidden))
        # Carry forward the ONNX hidden state for the next step.
        streaming_onnx_hidden = np.asarray(ort_step_hidden)

    # Print a success message if all comparisons passed.
    print("ONNX parity checks passed.")


if __name__ == "__main__":
    main()

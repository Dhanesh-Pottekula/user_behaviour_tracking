"""Export the trained PyTorch GRU model to ONNX format."""

# Enable postponed type-annotation evaluation.
from __future__ import annotations

# Torch loads the checkpoint and drives the ONNX exporter.
import torch

# Import checkpoint paths, ONNX output paths, and sequence length.
from config import CHECKPOINT_FILE, ONNX_DIR, ONNX_FILE, SEQ_LEN
# Import the GRU model and the ONNX-specific wrapper.
from model import BehaviorGRU, BehaviorGRUONNXWrapper


def main() -> None:
    """Load the trained model and export it as an ONNX graph."""

    # Load the saved checkpoint on CPU for export.
    checkpoint = torch.load(CHECKPOINT_FILE, map_location="cpu")

    # Recreate the model architecture with the saved dimensions.
    model = BehaviorGRU(
        input_size=checkpoint["feature_dim"],
        hidden_size=checkpoint["hidden_size"],
        num_classes=checkpoint["num_classes"],
    )
    # Load the trained weights.
    model.load_state_dict(checkpoint["model_state_dict"])
    # Switch to evaluation mode before export.
    model.eval()

    # Wrap the model so ONNX sees explicit input and hidden-state tensors.
    wrapper = BehaviorGRUONNXWrapper(model)
    # Ensure the ONNX output directory exists.
    ONNX_DIR.mkdir(parents=True, exist_ok=True)

    # Create a dummy sequence input for tracing the graph structure.
    dummy_input = torch.zeros(1, SEQ_LEN, checkpoint["feature_dim"], dtype=torch.float32)
    # Create a dummy initial hidden state for tracing recurrent state flow.
    dummy_h0 = torch.zeros(model.num_layers, 1, checkpoint["hidden_size"], dtype=torch.float32)

    # Export the model graph and parameters to an ONNX file.
    torch.onnx.export(
        wrapper,
        (dummy_input, dummy_h0),
        ONNX_FILE,
        export_params=True,
        opset_version=17,
        dynamo=False,
        input_names=["input", "h0"],
        output_names=["logits", "hn"],
        dynamic_axes={
            "input": {0: "batch_size", 1: "seq_len"},
            "h0": {1: "batch_size"},
            "logits": {0: "batch_size"},
            "hn": {1: "batch_size"},
        },
    )
    # Print the final ONNX path.
    print(f"exported onnx model: {ONNX_FILE}")


if __name__ == "__main__":
    main()

"""Evaluate the best saved checkpoint on the held-out test split."""

# Postpone annotation evaluation for cleaner type hints.
from __future__ import annotations

# Torch is used to load the checkpoint and run the model.
import torch
# Scikit-learn provides convenient text metrics for classification.
from sklearn.metrics import classification_report, confusion_matrix
# DataLoader batches the test samples.
from torch.utils.data import DataLoader

# Import checkpoint path, label mapping, and test split path.
from config import CHECKPOINT_FILE, ID_TO_LABEL, NUM_CLASSES, TEST_DATA_FILE
# Import the dataset wrapper.
from dataset import BehaviorDataset
# Import the GRU model definition.
from model import BehaviorGRU

# Use the GPU if available, otherwise CPU.
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def main() -> None:
    """Load the best checkpoint and report test metrics."""

    # Load the serialized training checkpoint.
    checkpoint = torch.load(CHECKPOINT_FILE, map_location=DEVICE)

    # Rebuild the model using the saved dimensions from the checkpoint.
    model = BehaviorGRU(
        input_size=checkpoint["feature_dim"],
        hidden_size=checkpoint["hidden_size"],
        num_classes=checkpoint["num_classes"],
    ).to(DEVICE)
    # Load the learned weights into the new model instance.
    model.load_state_dict(checkpoint["model_state_dict"])
    # Put the model in evaluation mode.
    model.eval()

    # Load the held-out test dataset.
    dataset = BehaviorDataset(str(TEST_DATA_FILE))
    # Build a deterministic test loader.
    loader = DataLoader(dataset, batch_size=64, shuffle=False)

    # Collect predicted class ids here.
    all_predictions: list[int] = []
    # Collect true class ids here.
    all_targets: list[int] = []

    # Turn off gradient tracking during evaluation.
    with torch.no_grad():
        # Iterate over the test set batch by batch.
        for X, y in loader:
            # Run the forward pass.
            logits, _ = model(X.to(DEVICE))
            # Append the predicted class ids.
            all_predictions.extend(logits.argmax(dim=1).cpu().tolist())
            # Append the true class ids.
            all_targets.extend(y.tolist())

    # Convert class ids back into readable label names.
    target_names = [ID_TO_LABEL[index] for index in range(NUM_CLASSES)]
    # Print the per-class precision, recall, and F1 report.
    print(classification_report(all_targets, all_predictions, target_names=target_names, digits=4))
    # Print the confusion matrix for a compact error summary.
    print(confusion_matrix(all_targets, all_predictions))


if __name__ == "__main__":
    main()

"""Offline training loop for the GRU behavior classifier."""

# Postpone annotation evaluation for cleaner type hints.
from __future__ import annotations

# Python's built-in RNG is seeded for reproducibility.
import random

# NumPy and Torch are both seeded because both may affect training behavior.
import numpy as np
import torch
import torch.nn as nn
# `DataLoader` batches dataset samples during training and validation.
from torch.utils.data import DataLoader

# Import paths, hyperparameters, and model dimensions.
from config import (
    BATCH_SIZE,
    CHECKPOINT_DIR,
    CHECKPOINT_FILE,
    EPOCHS,
    FEATURE_DIM,
    HIDDEN_SIZE,
    LEARNING_RATE,
    NUM_CLASSES,
    PREPROCESSING_METADATA_FILE,
    SEED,
    TRAIN_DATA_FILE,
    VAL_DATA_FILE,
    WEIGHT_DECAY,
)
# Import the dataset wrapper over preprocessed `.npz` files.
from dataset import BehaviorDataset
# Import the GRU model definition.
from model import BehaviorGRU

# Use a GPU if one is available, otherwise fall back to CPU.
DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")


def set_seed(seed: int) -> None:
    """Seed all RNGs used in this training script."""

    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)


def evaluate(model: BehaviorGRU, loader: DataLoader, criterion: nn.Module) -> tuple[float, float]:
    """Run a validation pass and return average loss and accuracy."""

    # Switch the model into evaluation mode.
    model.eval()
    # Accumulate total validation loss across batches.
    total_loss = 0.0
    # Count how many predictions are correct.
    total_correct = 0
    # Count how many examples have been seen.
    total_examples = 0

    # Disable gradient tracking to reduce memory and computation.
    with torch.no_grad():
        # Iterate over one validation batch at a time.
        for X, y in loader:
            # Move features to the active device.
            X = X.to(DEVICE)
            # Move labels to the active device.
            y = y.to(DEVICE)
            # Run a forward pass.
            logits, _ = model(X)
            # Compute the batch loss.
            loss = criterion(logits, y)

            # Add the batch loss scaled by batch size.
            total_loss += loss.item() * X.size(0)
            # Add the number of correct predictions in this batch.
            total_correct += (logits.argmax(dim=1) == y).sum().item()
            # Add the number of examples in this batch.
            total_examples += X.size(0)

    # Return dataset-level average loss and accuracy.
    return total_loss / total_examples, total_correct / total_examples


def main() -> None:
    """Train the model and save the best checkpoint."""

    # Make training as reproducible as possible.
    set_seed(SEED)
    # Ensure the checkpoint output directory exists.
    CHECKPOINT_DIR.mkdir(parents=True, exist_ok=True)

    # Load the preprocessed training split.
    train_dataset = BehaviorDataset(str(TRAIN_DATA_FILE))
    # Load the preprocessed validation split.
    val_dataset = BehaviorDataset(str(VAL_DATA_FILE))

    # Shuffle the training split so batches vary across epochs.
    train_loader = DataLoader(train_dataset, batch_size=BATCH_SIZE, shuffle=True)
    # Keep validation deterministic by disabling shuffle.
    val_loader = DataLoader(val_dataset, batch_size=BATCH_SIZE, shuffle=False)

    # Instantiate the GRU classifier.
    model = BehaviorGRU(
        input_size=FEATURE_DIM,
        hidden_size=HIDDEN_SIZE,
        num_classes=NUM_CLASSES,
    ).to(DEVICE)

    # Cross-entropy is the standard loss for multi-class classification.
    criterion = nn.CrossEntropyLoss()
    # AdamW handles gradient-based optimization with weight decay regularization.
    optimizer = torch.optim.AdamW(model.parameters(), lr=LEARNING_RATE, weight_decay=WEIGHT_DECAY)

    # Track the best validation accuracy seen so far.
    best_val_accuracy = 0.0
    # This will hold the checkpoint data for the best model.
    best_state = None

    # Loop over the dataset multiple times.
    for epoch in range(1, EPOCHS + 1):
        # Switch the model back to training mode.
        model.train()
        # Reset the running training loss accumulator.
        running_loss = 0.0

        # Process one training batch at a time.
        for X, y in train_loader:
            # Move features to the active device.
            X = X.to(DEVICE)
            # Move labels to the active device.
            y = y.to(DEVICE)

            # Clear the gradients from the previous optimization step.
            optimizer.zero_grad(set_to_none=True)
            # Run the forward pass through the model.
            logits, _ = model(X)
            # Compute the classification loss.
            loss = criterion(logits, y)
            # Backpropagate gradients through the network.
            loss.backward()
            # Clip gradients to reduce the chance of unstable updates.
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
            # Apply the optimizer step.
            optimizer.step()

            # Accumulate total training loss for this epoch.
            running_loss += loss.item() * X.size(0)

        # Convert total training loss into average training loss.
        train_loss = running_loss / len(train_dataset)
        # Evaluate on the validation set after the epoch.
        val_loss, val_accuracy = evaluate(model, val_loader, criterion)
        # Print an epoch summary for monitoring training progress.
        print(
            f"epoch={epoch:02d} "
            f"train_loss={train_loss:.4f} "
            f"val_loss={val_loss:.4f} "
            f"val_acc={val_accuracy:.4f}"
        )

        # If validation accuracy improved, remember this model state.
        if val_accuracy >= best_val_accuracy:
            best_val_accuracy = val_accuracy
            best_state = {
                "model_state_dict": model.state_dict(),
                "feature_dim": FEATURE_DIM,
                "hidden_size": HIDDEN_SIZE,
                "num_classes": NUM_CLASSES,
                "best_val_accuracy": best_val_accuracy,
                "metadata_path": str(PREPROCESSING_METADATA_FILE),
            }

    # Defensive check so we fail loudly if something went wrong during training.
    if best_state is None:
        raise RuntimeError("Training completed without producing a checkpoint.")

    # Save the best checkpoint to disk.
    torch.save(best_state, CHECKPOINT_FILE)
    # Print the checkpoint path for convenience.
    print(f"saved checkpoint: {CHECKPOINT_FILE}")
    # Print the best validation accuracy achieved during training.
    print(f"best validation accuracy: {best_val_accuracy:.4f}")


if __name__ == "__main__":
    main()

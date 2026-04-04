"""Dataset wrapper for preprocessed NumPy training splits."""

# Use postponed annotation evaluation for cleaner type hints.
from __future__ import annotations

# NumPy loads the `.npz` files created by preprocessing.
import numpy as np
# Torch tensors are what the model and DataLoader consume.
import torch
# `Dataset` is the base class expected by `torch.utils.data.DataLoader`.
from torch.utils.data import Dataset


class BehaviorDataset(Dataset):
    """Load one preprocessed split and expose it to PyTorch."""

    def __init__(self, path: str):
        """Read encoded features and labels from a `.npz` file."""

        # Load the saved arrays from disk.
        data = np.load(path)
        # Convert features into float tensors for the GRU.
        self.X = torch.tensor(data["X"], dtype=torch.float32)
        # Convert labels into integer class indices for cross-entropy loss.
        self.y = torch.tensor(data["y"], dtype=torch.long)

    def __len__(self) -> int:
        """Return the number of samples in this split."""

        return len(self.X)

    def __getitem__(self, index: int):
        """Return one `(features, label)` pair."""

        return self.X[index], self.y[index]

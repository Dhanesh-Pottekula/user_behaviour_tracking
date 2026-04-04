"""Model definitions for the user behavior tracker."""

# Enable postponed type-annotation evaluation.
from __future__ import annotations

# Torch provides tensors and neural-network modules.
import torch
import torch.nn as nn

# Import the configured number of GRU layers.
from config import NUM_GRU_LAYERS


class BehaviorGRU(nn.Module):
    """GRU-based classifier for user-behavior sequences."""

    def __init__(self, input_size: int, hidden_size: int, num_classes: int):
        """Create the recurrent model and output classifier."""

        # Initialize the parent `nn.Module`.
        super().__init__()
        # Store the hidden size for later shape construction.
        self.hidden_size = hidden_size
        # Store the number of output classes.
        self.num_classes = num_classes
        # Store the number of recurrent layers.
        self.num_layers = NUM_GRU_LAYERS

        # The GRU processes sequences of encoded user events.
        self.gru = nn.GRU(
            input_size=input_size,
            hidden_size=hidden_size,
            num_layers=self.num_layers,
            batch_first=True,
        )
        # The linear head converts the last GRU representation into class logits.
        self.classifier = nn.Linear(hidden_size, num_classes)

    def forward(self, x: torch.Tensor, h0: torch.Tensor | None = None):
        """Run one forward pass.

        Parameters:
        - `x`: event sequence tensor shaped `[batch, seq_len, feature_dim]`
        - `h0`: optional initial hidden state shaped `[layers, batch, hidden]`
        """

        # Run the recurrent network over the input sequence.
        outputs, hn = self.gru(x, h0)
        # Take the representation from the final time step for classification.
        logits = self.classifier(outputs[:, -1, :])
        # Return both logits and final hidden state so streaming inference can
        # keep carrying the hidden state across events.
        return logits, hn

    def initial_hidden(self, batch_size: int, device: torch.device | str) -> torch.Tensor:
        """Create an all-zero hidden state for a new batch or new session."""

        return torch.zeros(self.num_layers, batch_size, self.hidden_size, device=device)


class BehaviorGRUONNXWrapper(nn.Module):
    """Tiny wrapper used to expose explicit hidden-state I/O during ONNX export."""

    def __init__(self, model: BehaviorGRU):
        """Store the already-built GRU model to be exported."""

        super().__init__()
        self.model = model

    def forward(self, x: torch.Tensor, h0: torch.Tensor):
        """Forward the inputs directly into the wrapped model."""

        logits, hn = self.model(x, h0)
        return logits, hn

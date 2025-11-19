import torch
import torch.nn as nn

class AdapterLayer(nn.Module):
    def __init__(self, input_size, adapter_size):
        super(AdapterLayer, self).__init__()
        # First linear layer for dimensionality reduction
        self.down_project = nn.Linear(input_size, adapter_size)
        # ReLU activation function
        self.relu = nn.ReLU()
        # Second linear layer for dimensionality expansion
        self.up_project = nn.Linear(adapter_size, input_size)

    def forward(self, x):
        # Forward pass through Adapter layer
        down_projected = self.down_project(x)
        relu = self.relu(down_projected)
        up_projected = self.up_project(x)
        # Add Adapter output to input (residual connection)
        return x + up_projected

"""The Auto Encoder module."""

import torch.nn as nn
# import torch.nn.parallel as P
# import torch.utils.data


class SAE(nn.Module):
    """Stacked Auto Encoder class.

    Args:
    ----
    nb_labels : int
        The total number of labels
    in_f : int
        The total number of input features in the Linear layer, default=20
    out_f : int
        The total number of output features in the Linear layer, default=10
    """
    def __init__(self, nb_labels, in_f=20, out_f=10) -> None:
        super(SAE, self).__init__()

        # Fully connected layers
        self.fc1 = nn.Linear(nb_labels, in_f)
        self.fc2 = nn.Linear(in_f, out_f)
        self.fc3 = nn.Linear(out_f, in_f)
        self.fc4 = nn.Linear(in_f, nb_labels)

        # Define activation function
        self.activation = nn.Sigmoid()

    def forward(self, x0):
        """Transform input vector using full connection layers.

        Args:
        ----
        x0 : Tensor
            The input vector of features
        """
        # Encode input vector
        x1 = self.activation(self.fc1(x0))
        x2 = self.activation(self.fc2(x1))

        # Decode input vector
        x3 = self.activation(self.fc3(x2))
        x4 = self.fc4(x3)

        return x4

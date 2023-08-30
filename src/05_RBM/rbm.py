"""Construct a Restricted Boltzmann Machine model."""
from torch import (mm,
                   sum,
                   randn,
                   sigmoid,
                   bernoulli)


class RBM():
    """Create an instance of a Restricted Boltzmann Machine.

    Attributes
    ----------
    W : Tensor(nh, nv)
        Random normal distribution of weights
    a : Tensor(1, nh)
        Bias for the probability of hidden nodes given visible nodes
    b : Tensor(1, nv)
        Bias for the probability of visible nodes given hidden nodes
    """

    def __init__(self, nv, nh) -> None:
        """Initilize an RBM instance.

        Args:
        ----
        nv : int
            Number of visible nodes
        nh : int
            Number of hidden nodes
        """
        self.W = randn(nh, nv)
        self.a = randn(1, nh)
        self.b = randn(1, nv)

    def sample_h(self, x):
        """Sample activations of the hidden nodes, `p(h|v)`.

        Args:
        ----
        x : Tensor
            Values of visible neurons `v` in `p(h|v)`

        Returns:
        -------
        tuple(Tensor, Tensor)
            The probabilities the visible nodes equal 1 and
            the current sample of hidden node activations
        """
        # Get the product of x and self.W
        wx = mm(x, self.W.T)

        # Add the bias to each line of wx
        activation = wx + self.a.expand_as(wx)

        # Compute probabilities given the activations of visible nodes
        p_h_given_v = sigmoid(activation)

        # Return probabilities and sampling of p(h|v)
        return p_h_given_v, bernoulli(p_h_given_v)

    def sample_v(self, y):
        """Sample activations of the visible nodes, `p(v|h)`.

        Args:
        ----
        y : Tensor
            Values of hidden neurons `h` in `p(v|h)`

        Returns:
        -------
        tuple(Tensor, Tensor)
            The probabilities the hidden nodes equal 1 and
            the current sample of visible node activations
        """
        # Get the product of x and self.W
        wy = mm(y, self.W)

        # Add the bias to each line of wy
        activation = wy + self.b.expand_as(wy)

        # Compute probabilities given the activations of hidden nodes
        p_v_given_h = sigmoid(activation)

        # Return probabilities and sampling of p(v|h)
        return p_v_given_h, bernoulli(p_v_given_h)

    def train(self, v0, vk, ph0, phk):
        """Approximate the RBM log-likelihood gradient using contrastive
        divergence.

        Args:
        ----
        v0 : Tensor
            Ratings of all movies for one user
        vk : Tensor
            Visible nodes contained after `k` samplings
        ph0 : Tensor
            Vector of probabilities that hidden node equals 1 given `v0`
        phk : Tensor
            Vector of probabilities that hidden node equals 1 given `vk`
            after `k` samplings
        """
        self.W +=  (mm(v0.T, ph0) - mm(vk.T, phk)).T
        self.b += sum((v0 - vk), 0)
        self.a += sum((ph0 - phk), 0)

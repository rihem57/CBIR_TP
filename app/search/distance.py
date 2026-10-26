import numpy as np


def l1_distance(vector1, vector2):
    """
    Distance L1 / Manhattan.
    """

    return np.sum(np.abs(vector1 - vector2))


def l2_distance(vector1, vector2):
    """
    Distance L2 / Euclidienne.
    """

    return np.sqrt(
        np.sum((vector1 - vector2) ** 2)
    )
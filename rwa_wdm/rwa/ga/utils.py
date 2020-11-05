import logging
from typing import List

import numpy as np

__all__ = (
    'gof',
)

logger = logging.getLogger(__name__)


def gof(mat: np.ndarray, num_ch: int, route: List[int]) -> np.ndarray:
    """General objective function (GOF)

    Args:
        mat: Network's wavelength availability matrix
        num_ch: number of λ channels on each link
        route: the physical path as a sequence of router indices

    Returns:
        np.ndarray: GOF labels

    """
    L = np.zeros(num_ch + 1)  # GOF labels
    num_links = len(route) - 1  # GOF denominator Σ l_i
    for w in range(1, num_ch + 1):  # FIXME
        sum_weights = 0  # GOF numerator Σ w_λ
        # FIXME couldn't a chromosome be a Lightpath object?
        # That way I could use the `route.links` getter here.
        for i in range(num_links):
            rcurr = route[i]
            rnext = route[i + 1]
            sum_weights += w * mat[rcurr][rnext][w - 1]
            L[w - 1] = sum_weights / float(w * num_links)  # FIXME
    return L

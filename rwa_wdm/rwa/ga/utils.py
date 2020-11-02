import logging
from typing import List

import numpy as np

logger = logging.getLogger(__name__)


# FIXME FIXME FIXME
def get_wave_availability(k, n):
    return (int(n) & (1 << k)) >> k


def gof(mat: np.ndarray, num_ch: int, route: List[int]) -> np.ndarray:
    """General objective function

    """
    L = np.zeros(num_ch + 1)  # GOF labels
    num_links = len(route)  # GOF denominator Σ l_i
    for w in range(1, num_ch + 1):
        sum_weights = 0  # GOF numerator Σ w_λ
        # FIXME couldn't a chromosome be a Lightpath object?
        # That way I could use the `route.links` getter here.
        for i in range(num_links - 1):
            rcurr = route[i]
            rnext = route[i + 1]
            sum_weights += w * get_wave_availability(w - 1, mat[rcurr][rnext])
            L[w - 1] = sum_weights / float(w * (num_links - 1))  # FIXME
    return L

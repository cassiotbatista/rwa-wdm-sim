"""Random-fit wavelength assignment strategy

"""
from typing import List, Union

import numpy as np

# FIXME https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
from ...net import Network


def random_fit(net: Network, route: List[int]) -> Union[int, None]:
    """Random-fit algorithm

    Select a random wavelength index from the fixed set of available
    wavelengths

    Args:
        net: Network object
        route: path encoded as a sequence of router indices

    Returns:
        :obj:`int`: upon wavelength assignment success, return the wavelength
            index to be used on the lightpath

    """
    i, j = route[0], route[1]
    try:
        return np.random.choice(np.flatnonzero(net.n[i][j]))
    except ValueError:
        return None

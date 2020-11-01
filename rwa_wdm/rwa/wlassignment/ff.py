"""First-fit wavelength assignment strategy

"""

from typing import List, Union

# FIXME https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
from rwa_wdm.net import Network, Lightpath


def first_fit(net: Network, route: List[int]) -> Union[int, None]:
    """First fit algorithm

    """
    i, j = route[0], route[1]
    for w in range(net._num_channels):  # FIXME
        if net.get_wave_availability(w, net.n[i][j]):
            return w
    return None

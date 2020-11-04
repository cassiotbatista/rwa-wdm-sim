"""First-fit wavelength assignment strategy

"""

from typing import List, Union

# FIXME https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
from ...net import Network


def first_fit(net: Network, route: List[int]) -> Union[int, None]:
    """First fit algorithm

    """
    i, j = route[0], route[1]
    for w in range(net.nchannels):
        if net.n[i][j][w]:
            return w
    return None

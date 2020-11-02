from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class JointAcademicNetwork(Network):
    """U.K. Joint Academic Network (JANET)"""

    def __init__(self, ch_n):
        self._name = 'janet'
        self._fullname = u'Joint Academic Network'
        self._s = 1  # Manchester
        self._d = 6  # London
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [
            (0, 1), (0, 2),
            (1, 2), (1, 3),
            (2, 4),
            (3, 4), (3, 5),  # (3,6),
            (4, 6),
            (5, 6)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('Gla', (1.50, 4.00)),  # 0
            ('Man', (1.00, 3.00)),  # 1
            ('Lee', (2.00, 3.00)),  # 2
            ('Bir', (1.00, 2.00)),  # 3
            ('Not', (2.00, 2.00)),  # 4
            ('Bri', (1.00, 1.00)),  # 5
            ('Lon', (2.00, 1.00))   # 6
        ])

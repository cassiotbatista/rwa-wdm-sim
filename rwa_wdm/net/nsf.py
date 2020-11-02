from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class NationalScienceFoundation(Network):
    """U.S. National Science Foundation Network (NSFNET)"""

    def __init__(self, ch_n):
        self._name = 'nsf'
        self._fullname = u'National Science Foundation'
        self._s = 0
        self._d = 12
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [
            (0, 1), (0, 2), (0, 5),
            (1, 2), (1, 3),
            (2, 8),
            (3, 4), (3, 6), (3, 13),
            (4, 9),
            (5, 6), (5, 10),
            (6, 7),
            (7, 8),
            (8, 9),
            (9, 11), (9, 12),
            (10, 11), (10, 12),
            (11, 13)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('0', (0.70, 2.70)),   # 0
            ('1', (1.20, 1.70)),   # 1
            ('2', (1.00, 4.00)),   # 2
            ('3', (3.10, 1.00)),   # 3
            ('4', (4.90, 0.70)),   # 4
            ('5', (2.00, 2.74)),   # 5
            ('6', (2.90, 2.66)),   # 6
            ('7', (3.70, 2.80)),   # 7
            ('8', (4.60, 2.80)),   # 8
            ('9', (5.80, 3.10)),   # 9
            ('10', (5.50, 3.90)),  # 10
            ('11', (6.60, 4.60)),  # 11
            ('12', (7.40, 3.30)),  # 12
            ('13', (6.50, 2.40))   # 13
        ])

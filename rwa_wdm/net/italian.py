from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class Italian(Network):
    """Italian Network"""

    def __init__(self, ch_n):
        self._name = 'italian'
        self._fullname = u'Italian'
        self._s = 0  # FIXME
        self._d = 12
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [
            (0, 1), (0, 2),
            (1, 2), (1, 3), (1, 4),
            (2, 7), (2, 8), (2, 9),
            (3, 4), (3, 5),
            (4, 6), (4, 7),
            (5, 6),
            (6, 7),
            (7, 9), (7, 10),
            (8, 9), (8, 12),
            (9, 11), (9, 12),
            (10, 13),
            (11, 12), (11, 13),
            (12, 14), (12, 20),
            (13, 14), (13, 15),
            (14, 15), (14, 16), (14, 18), (14, 19),
            (15, 16),
            (16, 17),
            (17, 18),
            (18, 19),
            (19, 20)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('x', (0.70, 6.50)),  # 0
            ('x', (1.80, 7.00)),  # 1
            ('x', (1.80, 6.00)),  # 2
            ('x', (3.00, 7.70)),  # 3
            ('x', (2.70, 6.80)),  # 4
            ('x', (4.00, 6.70)),  # 5
            ('x', (3.30, 6.30)),  # 6
            ('x', (2.90, 5.70)),  # 7
            ('x', (2.00, 5.00)),  # 8
            ('x', (2.90, 5.00)),  # 9
            ('x', (3.80, 5.20)),  # 10
            ('x', (3.20, 4.50)),  # 11
            ('x', (2.50, 3.50)),  # 12
            ('x', (3.90, 4.00)),  # 13
            ('x', (3.70, 2.50)),  # 14
            ('x', (4.90, 3.00)),  # 15
            ('x', (4.50, 2.00)),  # 16
            ('x', (4.70, 1.00)),  # 17
            ('x', (3.80, 0.50)),  # 18
            ('x', (2.70, 0.60)),  # 19
            ('x', (1.20, 1.50))   # 20
        ])

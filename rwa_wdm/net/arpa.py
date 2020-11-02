from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class AdvancedResearchProjectsAgency(Network):
    """U.S. Advanced Research Projects Agency (ARPANET)"""

    def __init__(self, ch_n):
        self._name = 'arpa'
        self._fullname = u'Advanced Research Projects Agency'
        self._s = 0  # FIXME
        self._d = 12
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """Get edges as a list of tuples of pairs of nodes"""

        return [
            (0, 1), (0, 2), (0, 19),
            (1, 2), (1, 3),
            (2, 4),
            (3, 4), (3, 5),
            (4, 6),
            (5, 6), (5, 7),
            (6, 9),
            (7, 8), (7, 9), (7, 10),
            (8, 9), (8, 19),
            (9, 15),
            (10, 11), (10, 12),
            (11, 12),
            (12, 13),
            (13, 14), (13, 16),
            (14, 15),
            (15, 17), (15, 18),
            (16, 17), (16, 19),
            (17, 18)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('0', (1.80, 5.70)),   # 0
            ('1', (2.80, 5.00)),   # 1
            ('2', (3.40, 6.30)),   # 2
            ('3', (3.40, 5.50)),   # 3
            ('4', (4.50, 5.60)),   # 4
            ('5', (4.70, 4.60)),   # 5
            ('6', (5.30, 4.80)),   # 6
            ('7', (3.60, 4.40)),   # 7
            ('8', (2.20, 4.00)),   # 8
            ('9', (4.80, 3.50)),   # 9
            ('10', (2.40, 2.60)),  # 10
            ('11', (2.50, 1.50)),  # 11
            ('12', (1.40, 2.30)),  # 12
            ('13', (1.80, 3.20)),  # 13
            ('14', (3.70, 2.70)),  # 14
            ('15', (5.20, 2.50)),  # 15
            ('16', (0.80, 3.90)),  # 16
            ('17', (1.20, 0.50)),  # 17
            ('18', (3.60, 0.80)),  # 18
            ('19', (0.80, 5.50))   # 19
        ])

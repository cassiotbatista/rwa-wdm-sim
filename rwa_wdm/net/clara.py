from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class CooperacionLatinoAmericana(Network):
    """Cooperación Latino Americana de Redes Avanzadas (RedClara)"""

    def __init__(self, ch_n):
        self._name = 'clara'
        self._fullname = u'Cooperación Latino Americana de Redes Avanzadas'
        self._s = 3  # SV
        self._d = 9  # AR
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [
            (0, 1), (0, 5), (0, 8), (0, 11),
            (1, 2),
            (2, 3),
            (3, 4),
            (4, 5),
            (5, 6), (5, 7), (5, 11),
            (7, 8),
            (8, 9), (8, 11),
            (9, 10), (9, 11),
            (11, 12)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('US', (2.00, 6.00)),  # 0
            ('MX', (1.00, 6.00)),  # 1
            ('GT', (1.00, 4.50)),  # 2
            ('SV', (1.00, 2.50)),  # 3
            ('CR', (1.00, 1.00)),  # 4
            ('PN', (2.00, 1.00)),  # 5
            ('VE', (1.50, 1.70)),  # 6
            ('CO', (3.00, 1.00)),  # 7
            ('CL', (4.00, 1.00)),  # 8
            ('AR', (5.00, 3.50)),  # 9
            ('UY', (5.00, 1.00)),  # 10
            ('BR', (4.00, 6.00)),  # 11
            ('UK', (5.00, 6.00))   # 12
        ])

from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class RedeNacionalPesquisa(Network):
    """Rede (Brasileira) Nacional de Pesquisa (Rede Ipê / RNP)"""

    def __init__(self, ch_n):
        self._name = 'rnp'
        self._fullname = u'Rede Nacional de Pesquisas (Rede Ipê)'
        self._s = 3   # DF
        self._d = 11  # PE
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [
            (0, 1),
            (1, 3), (1, 4),
            (2, 4),
            (3, 4), (3, 7), (3, 17), (3, 19), (3, 25),
            (4, 6), (4, 12),
            (5, 25),
            (6, 7),
            (7, 8), (7, 11), (7, 18), (7, 19),
            (8, 9),
            (9, 10),
            (10, 11),
            (11, 12), (11, 13), (11, 15),
            (13, 14),
            (14, 15),
            (15, 16), (15, 19),
            (16, 17),
            (17, 18),
            (18, 19), (18, 20), (18, 22),
            (20, 21),
            (21, 22),
            (22, 23),
            (23, 24),
            (24, 25), (24, 26),
            (26, 27)
        ]

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('RR', (5.00, 3.25)),   # 0
            ('AM', (5.50, 3.75)),   # 1
            ('AP', (8.25, 3.75)),   # 2
            ('DF', (4.00, 5.00)),   # 3
            ('PA', (9.00, 3.00)),   # 4
            ('TO', (3.00, 3.00)),   # 5
            ('MA', (9.00, 4.00)),   # 6
            ('CE', (9.50,  5.00)),  # 7
            ('RN', (10.50, 5.00)),  # 8
            ('PB', (10.50, 3.00)),  # 9
            ('PB', (10.50, 1.00)),  # 10
            ('PE', (9.50,  1.00)),  # 11
            ('PI', (9.00, 2.00)),   # 12
            ('AL', (8.00, 2.00)),   # 13
            ('SE', (7.00, 2.00)),   # 14
            ('BA', (6.00, 2.00)),   # 15
            ('ES', (6.00, 1.00)),   # 16
            ('RJ', (4.00, 1.00)),   # 17
            ('SP', (2.00, 1.00)),   # 18
            ('MG', (6.00, 5.50)),   # 19
            ('SC', (1.00, 1.00)),   # 20
            ('RS', (1.00, 2.00)),   # 21
            ('PR', (2.00, 2.00)),   # 22
            ('MS', (2.00, 4.00)),   # 23
            ('MT', (2.00, 5.00)),   # 24
            ('GO', (3.00, 5.00)),   # 25
            ('RO', (1.00, 5.00)),   # 26
            ('AC', (1.00, 4.00))    # 27
        ])

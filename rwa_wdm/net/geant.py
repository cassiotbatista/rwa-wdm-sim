from typing import Dict, List, Tuple
from collections import OrderedDict

from . import Network


class GigabitEuropeanAcademic(Network):
    """Gigabit European Academic Network (GÉANT)"""

    def __init__(self, ch_n):
        self._name = 'geant'
        self._fullname = u'Gigabit European Academic Network'
        self._s = 3  # FIXME
        self._d = 9  # FIXME
        super().__init__(ch_n,
                         len(self.get_nodes_2D_pos()),
                         len(self.get_edges()))

    def get_edges(self) -> List[Tuple[int, int]]:
        """get"""

        return [ ]  # FIXME

    def get_nodes_2D_pos(self) -> Dict[str, Tuple[float, float]]:
        """Get position of the nodes on the bidimensional Cartesian plan"""

        return OrderedDict([
            ('AL', (9.5,   3.2)),  # 0      'ALBANIA',
            ('AM', (15.5,  3.1)),  # 1      'ARMENIA',
            ('AT', (8.1,   5.1)),  # 2      'AUSTRIA',
            ('AZ', (16.2,  3.1)),  # 3      'AZERBAIJAN',
            ('BE', (5.9,   6.2)),  # 4      'BELGIUM',
            ('BG', (10.8,  3.8)),  # 5      'BULGARIA',
            ('BY', (11.3,  6.9)),  # 6      'BELARUS',
            ('CH', (6.8,   4.8)),  # 7      'SWITZERLAND',
            ('CY', (12.8,  1.5)),  # 8      'CYPRUS',
            ('CZ', (8.2,   5.9)),  # 9      'CZECH REPUBLIC',
            ('DE', (7.0,   6.0)),  # 10     'GERMANY',
            ('DK', (7.0,   7.9)),  # 11     'DENMARK',
            ('EE', (10.9,  8.8)),  # 12     'ESTONIA',
            ('ES', (4.0,   3.0)),  # 13     'SPAIN',
            ('FI', (11.0, 10.3)),  # 14     'FINLAND',
            ('FR', (5.5,   4.9)),  # 15     'FRANCE',
            ('GE', (15.0,  3.7)),  # 16     'GEORGIA',
            ('GR', (10.2,  2.5)),  # 17     'GREECE',
            ('HR', (8.9,   4.6)),  # 18     'CROATIA',
            ('HU', (9.8,   5.0)),  # 19     'HUNGARY',
            ('IE', (2.9,   6.9)),  # 20     'IRELAND',
            ('IL', (13.1,  0.6)),  # 21     'ISRAEL',
            ('IS', (0.6,  11.1)),  # 22     'ICELAND',
            ('IT', (7.5,   4.0)),  # 23     'ITALY',
            ('LT', (10.9,  7.5)),  # 24     'LITHUANIA',
            ('LU', (6.2,   5.7)),  # 25     'LUXEMBOURG',
            ('LV', (10.9,  8.1)),  # 26     'LATVIA',
            ('MD', (11.7,  5.0)),  # 27     'MOLDOVA',
            ('ME', (9.3,   3.7)),  # 28     'MONTENEGRO',
            ('MK', (10.0,  3.3)),  # 29     'MACEDONIA',
            ('MT', (8.2,   1.8)),  # 30     'MALTA',
            ('NL', (6.0,   6.8)),  # 31     'NETHERLANDS',
            ('NO', (6.5,  10.0)),  # 32     'NORWAY',
            ('PL', (9.2,   6.5)),  # 33     'POLAND',
            ('PT', (2.9,   3.0)),  # 34     'PORTUGAL',
            ('RO', (11.1,  4.3)),  # 35     'ROMANIA',
            ('RS', (9.7,   4.2)),  # 36     'SERBIA',
            ('SE', (8.6,   9.5)),  # 37     'SWEDEN',
            ('SI', (8.2,   4.6)),  # 38     'SLOVENIA ',
            ('SK', (9.1,   5.5)),  # 39     'SLOVAKIA',
            ('TR', (12.1,  3.0)),  # 40     'TURKEY',
            ('UK', (4.4,   6.9)),  # 41     'UNITED KINGDOM',
            ('UA', (11.8,  6.0)),  # 42     'UKRAINE',
        ])

"""Implements network topologies

"""

__author__ = 'Cassio Batista'

import logging
from itertools import count
from typing import Iterable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)


class Lightpath(object):
    """Emulates a lightpath composed by a route and a wavelength channel

    """

    # https://stackoverflow.com/questions/8628123/counting-instances-of-a-class
    _ids = count(0)

    def __init__(self, route: List[int], wavelength: int):
        self._id: int = next(self._ids)
        self._route: List[int] = route
        self._wavelength: int = wavelength
        self._holding_time: float = 0.0

    @property
    def id(self) -> int:
        return self._id

    @property
    def r(self) -> List[int]:
        return self._route

    # https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    # pairwise: https://docs.python.org/3/library/itertools.html
    @property
    def links(self) -> Iterable[Tuple[int, int]]:
        iterable = iter(self._route)
        while True:
            try:
                yield next(iterable), next(iterable)
            except StopIteration:
                return

    def add_router(self, router: int) -> None:
        self._route.append(router)

    @property
    def w(self) -> int:
        return self._wavelength

    @property
    def holding_time(self) -> float:
        return self._holding_time

    @holding_time.setter
    def holding_time(self, time: float) -> None:
        self._holding_time = time

    def __len__(self):
        return len(self.r)

    def __str__(self):
        return '%s %d' % (self._route, self._wavelength)


class AdjacencyMatrix(np.ndarray):
    """2D array of boolean-valued neighbourhood information

    """

    def __new__(cls, num_nodes):
        arr = np.zeros((num_nodes, num_nodes))
        obj = np.asarray(arr, dtype=np.bool).view(cls)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return


class WavelengthAvailabilityMatrix(np.ndarray):
    """3D array of int16-valued availability units

    """

    def __new__(cls, num_nodes, num_ch):
        arr = np.zeros((num_nodes, num_nodes, num_ch))
        obj = np.asarray(arr, dtype=np.bool).view(cls)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return


class TrafficMatrix(np.ndarray):
    """3D array of float32-valued timestamps

    """

    def __new__(cls, num_nodes, num_ch):
        arr = np.zeros((num_nodes, num_nodes, num_ch))
        obj = np.asarray(arr, dtype=np.float32).view(cls)

        # set extra parameters
        obj._usage: np.ndarray = np.zeros(num_ch, dtype=np.uint16)
        obj._lightpaths: List[Lightpath] = []

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return
        self._usage = getattr(obj, "_usage", None)
        self._lightpaths = getattr(obj, "_lightpaths", None)

    @property
    def lightpaths(self) -> List[Lightpath]:
        return self._lightpaths

    @property
    def num_conns(self):
        return len(self._lightpaths)

    def usage(self, wavelength: int) -> np.uint16:
        return self._usage[wavelength]

    def add_lightpath(self, lightpath: Lightpath) -> None:
        self._lightpaths.append(lightpath)

    # FIXME this seems silly, but...
    # https://stackoverflow.com/questions/9140857/oop-python-removing-class-instance-from-a-list/9140906
    def remove_lightpath_by_id(self, _id: int) -> None:
        for i, lightpath in enumerate(self.lightpaths):
            if lightpath.id == _id:
                del self._lightpaths[i]
                break


class Network(object):
    """Network base class"""

    def __init__(self, num_channels, num_nodes, num_links):
        self._num_channels = num_channels
        self._num_nodes = num_nodes
        self._num_links = num_links

        self._n = WavelengthAvailabilityMatrix(self._num_nodes,
                                               self._num_channels)
        self._a = AdjacencyMatrix(self._num_nodes)
        self._t = TrafficMatrix(self._num_nodes, self._num_channels)

        # fill in wavelength availability matrix
        for (i, j) in self.get_edges():
            for w in range(self._num_channels):
                availability = np.random.choice((0, 1))
                self._n[i][j][w] = availability
                self._n[j][i][w] = self._n[i][j][w]

        # fill in adjacency matrix
        for (i, j) in self.get_edges():
            neigh = 1
            self._a[i][j] = neigh
            self._a[j][i] = self._a[i][j]

        # fill in traffic matrix
        # FIXME when updating the traffic matrix via holding time parameter,
        # these random time attributions may seem not the very smart ones,
        # since decreasing values by until_next leads T to be uneven and
        # unbalanced
        for (i, j) in self.get_edges():
            for w in range(self._num_channels):
                random_time = self._n[i][j][w] * np.random.rand()
                self._t[i][j][w] = random_time
                self._t[j][i][w] = self._t[i][j][w]

    # Children are responsible for overriding this method
    def get_edges(self):
        raise NotImplementedError

    # Children are responsible for overriding this method
    def get_nodes_2D_pos(self):
        raise NotImplementedError

    @property
    def n(self) -> np.ndarray:
        return self._n

    @property
    def a(self) -> np.ndarray:
        return self._a

    @property
    def t(self) -> np.ndarray:
        return self._t

    @property
    def s(self) -> int:
        return self._s

    @property
    def d(self) -> int:
        return self._d

    @property
    def name(self) -> str:
        return self._name

    @property
    def nchannels(self) -> int:
        return self._num_channels

    @property
    def nnodes(self) -> int:
        return self._num_nodes

    @property
    def nlinks(self) -> int:
        return self._num_links

    def plot_topology(self, bestroute=False) -> None:
        fig = plt.figure()
        ax = fig.add_subplot(111)

        # define vertices or nodes as points in 2D cartesian plan
        # define links or edges as node index ordered pairs in cartesian plan
        nodes = self.get_nodes_2D_pos()
        links = self.get_edges()
        ax.grid()

        # draw edges before vertices
        # FIXME this won't work
        for (i, j) in links:
            x = [nodes[i][0], nodes[j][0]]
            y = [nodes[i][1], nodes[j][1]]
            plt.plot(x, y, 'k', linewidth=2)

        # highlight in red the shortest path with wavelength(s) available
        # a.k.a. 'best route'
        if isinstance(bestroute, list):
            for i in range(len(bestroute) - 1):
                x = [nodes[bestroute[i]][0], nodes[bestroute[i + 1]][0]]
                y = [nodes[bestroute[i]][1], nodes[bestroute[i + 1]][1]]
                plt.plot(x, y, 'r', linewidth=2.5)

        # draw vertices
        for label, (i, j) in nodes.items():
            plt.plot(i, j, 'wo', markersize=25)
            ax.annotate(label, xy=(i, j), ha='center', va='center')

        # adjust values over both x and y axis
        plt.xticks(np.arange(0, 9, 1))
        plt.yticks(np.arange(0, 7, 1))

        # finally, show the plotted graph
        plt.show(block=True)

"""Implements network topologies

"""

__author__ = 'Cassio Batista'

import logging
from itertools import count
from operator import itemgetter
from typing import Iterable, List, Tuple

import numpy as np
import matplotlib.pyplot as plt

__all__ = (
    'Lightpath',
    'AdjacencyMatrix',
    'WavelengthAvailabilityMatrix',
    'TrafficMatrix',
    'Network',
)

logger = logging.getLogger(__name__)


class Lightpath(object):
    """Emulates a lightpath composed by a route and a wavelength channel

    Lightpath is pretty much a regular path, but must also specify a wavelength
    index, since WDM optical networks span multiple wavelength channels over a
    single fiber link on the topology.

    A Lightpath object also store a holding time parameter, which is set along
    the simulation to specify how long the connection may be alive and running
    on network links, and therefore taking up space in the traffic matrix,
    before it finally terminates and resources are deallocated.

    Args:
        route: a liste of nodes encoded as integer indices
        wavelength: a single number representing the wavelength channel index

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
        """A unique identifier to the Lightpath object"""
        return self._id

    @property
    def r(self) -> List[int]:
        """The path as a sequence of router indices"""
        return self._route

    # https://stackoverflow.com/questions/5389507/iterating-over-every-two-elements-in-a-list
    # pairwise: https://docs.python.org/3/library/itertools.html
    @property
    def links(self) -> Iterable[Tuple[int, int]]:
        """Network links as a sequence of pairs of nodes"""
        iterable = iter(self._route)
        while True:
            try:
                yield next(iterable), next(iterable)
            except StopIteration:
                return

    @property
    def w(self) -> int:
        """The wavelength channel index"""
        return self._wavelength

    @property
    def holding_time(self) -> float:
        """Time that the lightpath remains occupying net resources"""
        return self._holding_time

    @holding_time.setter
    def holding_time(self, time: float) -> None:
        self._holding_time = time

    def __len__(self):
        return len(self.r)

    def __str__(self):
        return '%s %d' % (self._route, self._wavelength)


class AdjacencyMatrix(np.ndarray):
    """Boolean 2D matrix that stores network neighbourhood info

    The adjacency matrix is basically a binary, bidimensional matrix that
    informs whether two nodes in a network physical topology are neighbours,
    i.e,. share a link connection. This class is a subclass of a NumPy array.

    Args:
        num_nodes: number of nodes in the network, which define a square
            matrix's dimensions

    """

    def __new__(cls, num_nodes: int):
        arr = np.zeros((num_nodes, num_nodes))
        obj = np.asarray(arr, dtype=np.bool).view(cls)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return


class WavelengthAvailabilityMatrix(np.ndarray):
    """Boolean 3D matrix that stores network wavelength availability info

    The wavelength availability matrix is a tridimensional, binary matrix that
    stores information on whether a particular wavelength λ is available on an
    optical link (i, j). This class is a subclass of a NumPy array.

    Args:
        num_nodes: number of nodes in the network, which defines two of the
            matrix's dimensions
        num_ch: number of wavelength channels on each link, defining the shape
            of the third dimension of the matrix

    """

    def __new__(cls, num_nodes: int, num_ch: int):
        arr = np.zeros((num_nodes, num_nodes, num_ch))
        obj = np.asarray(arr, dtype=np.bool).view(cls)

        return obj

    def __array_finalize__(self, obj):
        if obj is None:
            return


class TrafficMatrix(np.ndarray):
    """Boolean 3D matrix that stores traffic info

    Args:
        num_nodes: number of nodes in the network, which defines two of the
            matrix's dimensions
        num_ch: number of wavelength channels on each link, defining the shape
            of the third dimension of the matrix

    """

    def __new__(cls, num_nodes: int, num_ch: int):
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
        """The list of connections (lightpaths) currently running"""
        return self._lightpaths

    @property
    def nconns(self):
        """The number of connections (lightpaths) currently running"""
        return len(self._lightpaths)

    def add_lightpath(self, lightpath: Lightpath) -> None:
        """Add a lightpath to the list of lightpath

        Args:
            lightpath: a Lightpath instance

        """
        self._lightpaths.append(lightpath)

    # FIXME this seems silly, but...
    # https://stackoverflow.com/questions/9140857/oop-python-removing-class-instance-from-a-list/9140906
    def remove_lightpath_by_id(self, _id: int) -> None:
        """Remove a lightpath from the list of currently running connections

        Args:
            _id: the unique identifier of a lightpath

        """
        for i, lightpath in enumerate(self.lightpaths):
            if lightpath.id == _id:
                del self._lightpaths[i]
                break


class Network(object):
    """Network base class

    Hols network properties such as adjacency, wavelength-availability and
    traffic graph matrices, fixed source and destination nodes for all
    connections, number of λ channels per link

    Args:
        num_channels: number of wavelength channels per link
        num_nodes: number of routes along the path
        num_links: number of links along the path, typically `num_nodes` - 1

    """

    def __init__(self,
                 num_channels: int, num_nodes: int, num_links: int) -> None:
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
        """The wavelength availability matrix graph"""
        return self._n

    @property
    def a(self) -> np.ndarray:
        """The adjacency matrix graph"""
        return self._a

    @property
    def t(self) -> np.ndarray:
        """The traffic matrix"""
        return self._t

    @property
    def s(self) -> int:
        """The source node"""
        return self._s

    @property
    def d(self) -> int:
        """The destination node"""
        return self._d

    @property
    def name(self) -> str:
        """The short name tag idenfier of the network topology"""
        return self._name

    @property
    def nchannels(self) -> int:
        """The number of wavelength channels per fiber link"""
        return self._num_channels

    @property
    def nnodes(self) -> int:
        """The number of router nodes (vertices) in the network"""
        return self._num_nodes

    @property
    def nlinks(self) -> int:
        """The number of links (edges) in the network"""
        return self._num_links

    def plot_topology(self, bestroute: List[int] = None) -> None:
        """Plots the physical topology in a 2D Cartesian plan

        Args:
            bestroute: a route encoded as a list of router indices to be
                highlighted in red over some network edges

        """
        fig, ax = plt.subplots()
        ax.grid()

        # define vertices or nodes as points in 2D cartesian plan
        # define links or edges as node index ordered pairs in cartesian plan
        links = self.get_edges()
        nodes = self.get_nodes_2D_pos()
        node_coords = list(nodes.values())  # get only 2D coordinates

        # draw edges before vertices
        for (i, j) in links:
            x = (node_coords[i][0], node_coords[j][0])
            y = (node_coords[i][1], node_coords[j][1])
            ax.plot(x, y, 'k', lw=2)

        # highlight in red the shortest path with wavelength(s) available
        # a.k.a. 'best route'
        if bestroute is not None:
            for i in range(len(bestroute) - 1):
                rcurr, rnext = bestroute[i], bestroute[i + 1]
                x = (node_coords[rcurr][0], node_coords[rnext][0])
                y = (node_coords[rcurr][1], node_coords[rnext][1])
                ax.plot(x, y, 'r', lw=3)

        # draw vertices
        for label, (i, j) in nodes.items():
            ax.plot(i, j, 'wo', ms=25, mec='k')
            ax.annotate(label, xy=(i, j), ha='center', va='center')

        # https://stackoverflow.com/questions/13145368/find-the-maximum-value-in-a-list-of-tuples-in-python
        xlim = np.ceil(max(node_coords, key=itemgetter(0))[0]) + 2
        ylim = np.ceil(max(node_coords, key=itemgetter(1))[1]) + 2
        if self.name == 'nsf':
            xlim -= 1  # FIXME gambiarra, hehe. NSF needs redrawing

        # adjust values over both x and y axis
        ax.set_xticks(np.arange(xlim))
        ax.set_yticks(np.arange(ylim))

        # finally, show the plotted graph
        plt.show(block=True)

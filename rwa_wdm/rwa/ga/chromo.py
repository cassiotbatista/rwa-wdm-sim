"""Classes related to individuals and their fitness

"""
import logging
from itertools import count
from typing import List

import numpy as np

__all__ = (
    'Fitness',
    'Chromosome'
)

logger = logging.getLogger(__name__)
np.set_printoptions(precision=2)


class Fitness(object):
    """Fitness 'namedtuple'-like object

    Easy to handle ready-to-use properties such as number of wavelengths
    available per route, and number of hops in the route.

    Args:
        labels: general objective function (GOF)'s label `L`
        lambdas: number of wavelengths available on a single link
        hops: number of hops in the route

    """

    def __init__(self, labels: np.ndarray, lambdas: int, hops: int) -> None:
        self._gof_labels: np.ndarray = labels
        self._num_wavelenths_available: int = lambdas
        self._route_length: int = hops

    @property
    def labels(self) -> np.ndarray:
        """The labels `L` produced by the general objective function (GOF)"""
        return self._gof_labels

    @labels.setter
    def labels(self, value: np.ndarray) -> None:
        self._gof_labels = value

    @property
    def lambdas(self) -> int:
        """The total number of λ available on a single link"""
        return self._num_wavelenths_available

    @lambdas.setter
    def lambdas(self, value: int) -> None:
        self._num_wavelenths_available = value

    @property
    def hops(self) -> int:
        """The number of hops comprising a route"""
        return self._route_length

    @hops.setter
    def hops(self, value: int) -> None:
        self._route_length = value

    def __str__(self) -> str:
        return '{} {} {}'.format(self.labels, self.lambdas, self.hops)


class Chromosome(object):
    """Encodes an invididual with genes and a fitness attribute

    Args:
        genes: sequence of router indices comprising a route
        fitness: a Fitness object comprising GOF labels, number of λ available,
            and number of hops

    """
    _ids = count(0)

    def __init__(self, genes: List[int],
                 fitness: Fitness = None) -> None:
        self._id: int = next(self._ids)
        self._genes: List[int] = genes
        self._fitness: Fitness = fitness

    @property
    def id(self) -> int:
        """A unique identifier to the Chromosome object"""
        return self._id

    @property
    def genes(self) -> List[int]:
        """The route encoded as chromosome's genes"""
        return self._genes

    @property
    def fit(self) -> Fitness:
        """The Fitness object"""
        return self._fitness

    @fit.setter
    def fit(self, value: Fitness) -> None:
        self._fitness = value

    def __len__(self) -> int:
        return len(self._genes)

    def __str__(self) -> str:
        return '%s (%s)' % (self.genes, self.fit)

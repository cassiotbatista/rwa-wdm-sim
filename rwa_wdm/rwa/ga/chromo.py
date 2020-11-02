import logging
from itertools import count
from typing import List

import numpy as np

logger = logging.getLogger(__name__)
np.set_printoptions(precision=2)


class Fitness(object):
    """Fitness 'namedtuple'-like object

    Easy to handle ready-to-use properties such as number of wavelengths
    available per route, and number of hops in the route.
    """

    def __init__(self,
                 labels: List[int] = None,
                 lambdas: int = None,
                 hops: int = None) -> None:
        self._gof_labels: List[int] = labels
        self._num_wavelenths_available: int = lambdas
        self._route_length: int = hops

    @property
    def labels(self) -> List[int]:
        return self._gof_labels

    @labels.setter
    def labels(self, value: List[int]) -> None:
        self._gof_labels = value

    @property
    def lambdas(self) -> int:
        return self._num_wavelenths_available

    @lambdas.setter
    def lambdas(self, value: int) -> None:
        self._num_wavelenths_available = value

    @property
    def hops(self) -> int:
        return self._route_length

    @hops.setter
    def hops(self, value: int) -> None:
        self._route_length = value

    def __str__(self) -> str:
        return '{} {} {}'.format(self.labels, self.lambdas, self.hops)


class Chromosome(object):
    """Encodes an invididual with genes and a fitness attribute

    """

    _ids = count(0)

    def __init__(self,
                 genes: List[int] = [],
                 fitness: Fitness = None) -> None:
        self._id: int = next(self._ids)
        self._genes: List[int] = genes
        self._fitness: Fitness = fitness

    @property
    def id(self) -> int:
        return self._id

    @property
    def genes(self) -> List[int]:
        return self._genes

    def add_gene(self, gene: int) -> None:
        self._genes.append(gene)

    @property
    def fit(self) -> Fitness:
        return self._fitness

    @fit.setter
    def fit(self, value: Fitness) -> None:
        self._fitness = value

    def __len__(self) -> int:
        return len(self._genes)

    def __str__(self) -> str:
        return '%s (%s)' % (self.genes, self.fit)

"""Population holds a set of individuals

"""
from __future__ import annotations

import copy
import logging
from typing import List, Set, Union

import numpy as np

from .chromo import Chromosome

__all__ = (
    'Population',
)

logger = logging.getLogger(__name__)


class Population(object):
    """Class to store a collection of Chromosome objects

    Population is also responsible for sorting chromosomes by their fitness
    values, always keeping tracking of the best one.

    """
    def __init__(self):
        self._individuals: List[Chromosome] = []


    # 1: Start from source node
    # 2: Randomly choose, with equal probability, one of the nodes
    #    that is surely connected to the current node to be the next in path
    # 3: If the chosen node hasn't been visited before, mark it as the
    #    next in the path (gene). Otherwise find another node
    # 6: Do this until the destination node is found
    def make_chromosome(self, mat: np.ndarray,
                        s: int, d: int, allels: Set[int],
                        max_size: int) -> Union[None, Chromosome]:
        """Creates a single Chromosome via DFS-like procedure

        Args:
            mat: Network's wavelength availability matrix
            s: source node of the connection
            d: destination node of the connection
            allels: values the chromosome's genes are allowed to assume, which
                basically comprises router indices
            max_size: value to prevent chromosomes from being too long

        Returns:
            Chromosome: returns an individual if random procedure is
                successfull

        """
        trial = 0
        reset = 0
        rcurr = s  # step 1
        allels = list(allels)
        genes = [allels.pop(allels.index(rcurr))]
        while rcurr != d:  # step 6
            rnext = np.random.choice(allels)  # step 2
            if mat[rcurr][rnext]:  # ensure neighbourhood
                rcurr = rnext  # step 3
                genes.append(allels.pop(allels.index(rcurr)))
                trial = 0
            else:
                trial += 1
                if trial > 50:  # chances per gene to find a valid path
                    while genes[-1] != s:
                        allels.append(genes.pop())
                    trial = 0
                    reset += 1
                    if reset == 5:
                        return None

        if len(genes) > max_size:
            return None
        return Chromosome(genes)

    def add_chromosome(self, chromosome: Chromosome) -> None:
        """Adds a Chromosome into the population

        Args:
            chromosome: an individual encoded as a Chromosome instance

        """
        self._individuals.append(chromosome)

    def remove_chromosome_by_id(self, _id: int) -> None:
        """Removes a Chromosome from the population

        Args:
            _id: unique index identifying a particular individual

        """
        for i, chromosome in enumerate(self._individuals):
            if chromosome.id == _id:
                del self._individuals[i]
                break

    @property
    def individuals(self) -> List[Chromosome]:
        """The population as a sequence of Chromosomes"""
        return self._individuals

    @property
    def best(self) -> Chromosome:
        """The fittest chromosome (requires sorting)"""
        return self._individuals[0]

    def copy(self) -> Population:
        """Deep copy of the Population's own instance"""
        return copy.deepcopy(self)

    # https://stackoverflow.com/questions/403421/how-to-sort-a-list-of-objects-based-on-an-attribute-of-the-objects
    def sort(self) -> int:
        """Sorts the population following some criteria

        Returns:
            :obj: `int`: number of fit individuals, i.e., with at least one λ
                available on each link

        """
        # sort according to λ availability .:. least congested paths first
        self.individuals.sort(key=lambda x: x.fit.lambdas, reverse=True)

        # sort according to number of hops .:. shortest paths first
        for j in range(1, len(self.individuals)):
            chrom = self.individuals[j]
            i = j - 1
            if chrom.fit.lambdas:
                while i >= 0 and self.individuals[i].fit.hops > chrom.fit.hops:
                    self.individuals[i + 1] = self.individuals[i]
                    i -= 1
                self.individuals[i + 1] = chrom

        # FIXME this wasn't supposed to be here, yet...
        # compute the number of individuals with at least one λ available
        fit = 0
        for individual in self.individuals:
            if individual.fit.lambdas:
                fit += 1
        return fit

    def __len__(self) -> int:
        return len(self._individuals)

import logging
from typing import List, Tuple, Union

from .pop import Population
from .env import evaluate, select, cross, mutate
from ...net import Network

logger = logging.getLogger(__name__)


class GeneticAlgorithm(object):
    """Genetic algorithm

    """

    def __init__(self, pop_size, num_gen, cross_rate, mut_rate) -> None:
        self._population_size: int = pop_size
        self._num_generations: int = num_gen
        self._crossover_rate: float = cross_rate
        self._mutation_rate: float = mut_rate
        self._best_fits = []

    @property
    def bestfit(self) -> List[int]:
        return self._best_fits

    # FIXME not sure this will work for the '+=' operator
    @bestfit.setter
    def bestfit(self, value: int) -> None:
        self._best_fits.append(value)

    def run(self, net: Network, k: int) -> Tuple[List[int], Union[int, None]]:
        # generates initial population with random but valid chromosomes
        population = Population()
        trial = 0
        logger.debug('Creating population')
        while len(population) < self._population_size and trial < 300:  # FIXME
            allels = set(range(net.nnodes))  # router indexes
            chromosome = population.make_chromosome(net.a, net.s, net.d,
                                                    allels, net.nnodes)
            if chromosome is not None:
                population.add_chromosome(chromosome)
                trial = 0
            else:
                trial += 1

        logger.debug('Initiating GA main loop')
        for generation in range(self._num_generations + 1):
            # perform evaluation (fitness calculation)
            logger.debug('Gen %d: fitness evaluation' % generation)
            for chromosome in population.individuals:
                chromosome.fit = evaluate(net, chromosome)

            # sort in-place by fitness considering λ avail. and route length
            logger.debug('Gen %d: sort by fitness' % generation)
            self.bestfit = population.sort()  # FIXME

            # avoid ugly evaluation and sort after loop
            if generation == self._num_generations:
                break

            # perform selection
            logger.debug('Gen %d: applying selection operator' % generation)
            mating_pool = select(population.copy(), self._population_size)

            # perform crossover over the lucky ones selected to the mating pool
            logger.debug('Gen %d: applying crossover operator' % generation)
            offspring = cross(mating_pool, self._population_size,
                              self._crossover_rate)

            # perform mutation over offspring, overwriting original population
            logger.debug('Gen %d: applying mutation operator' % generation)
            population = mutate(offspring, self._population_size,
                                self._mutation_rate, net)

        route = population.best.genes
        try:
            wavelength = population.best.fit.labels.tolist().index(1)
        except ValueError:
            wavelength = None
        return route, wavelength

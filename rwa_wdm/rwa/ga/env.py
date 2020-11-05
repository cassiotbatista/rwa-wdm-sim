"""Environment related procedures

"""
import logging
import numpy as np

from .utils import gof
from .chromo import Chromosome, Fitness
from .pop import Population
from ...net import Network

__all__ = (
    'evaluate',
    'select',
    'cross',
    'mutate',
)

logger = logging.getLogger(__name__)


def evaluate(net: Network, chromosome: Chromosome) -> Fitness:
    """Fitness calculation

    Args:
        net: Network instance object
        chromosome: Chromosome object

    Returns:
        Fitness: Fitness object storing GOF labels, number of λ available per
            link, and number of hops in the route

    """
    labels = gof(net.n, net.nchannels, chromosome.genes)
    lambdas_available = np.count_nonzero(labels == 1.0)
    route_length = len(chromosome)

    return Fitness(labels, lambdas_available, route_length)


def select(population: Population,
           pop_size: int, tourn_size: int = 3) -> Population:
    """Tournament selection strategy

    First we choose a random candidate from population. Then, under trials,
    we choose another candidate and compare the two fitnesses. The winner
    becomes the top candidate; loser is eliminated.

    Args:
        population: Population instance object after evaluation
        pop_size: number of individuals in the mating pool pre-crossover
        tourn_size: number of individuals to compete under the tournament pool

    Returns:
        Population: set of parents ready to mate under crossover operation

    """
    parents = Population()
    while len(parents) < pop_size:
        candidates = [np.random.choice(population.individuals)]
        for trial in range(tourn_size):
            candidates.append(np.random.choice(population.individuals))
            if candidates[0].fit.lambdas >= candidates[1].fit.lambdas:
                candidates.remove(candidates[1])
            else:
                candidates.remove(candidates[0])
        parents.add_chromosome(candidates[0])
    return parents


def cross(parents: Population, pop_size: int, tc: float) -> Population:
    """One-point crossover strategy

    Args:
        parents: set of chromosomes ready to mate
        pop_size: number of individuals in the offspring after crossover
        tc: crossover rate, which defines the percentage of the selected
            individuals to undergo crossover

    Returns:
        Population: set of children in offspring to undergo mutation operation

    """
    children = Population()
    while len(children) < pop_size:
        # choose parents and make sure they are differente ones
        # TODO parents.pop(np.random.randint(len(parents))) ?
        dad = np.random.choice(parents.individuals)
        mom = np.random.choice(parents.individuals)
        parents.remove_chromosome_by_id(dad.id)
        parents.remove_chromosome_by_id(mom.id)
        dad = dad.genes
        mom = mom.genes
        if tc > np.random.random():
            # common nodes between father and mother, excluding s and d
            ridx = []
            for gene in dad[1:len(dad) - 1]:
                if gene in mom[1:len(mom) - 1]:
                    ridx.append([dad.index(gene), mom.index(gene)])

                # randomly choose a common node index to be the crossover point
                if len(ridx):
                    rcommon = ridx.pop(np.random.choice(len(ridx)))
                    son = dad[:rcommon[0]] + mom[rcommon[1]:]
                    daughter = mom[:rcommon[1]] + dad[rcommon[0]:]
                else:
                    son = dad
                    daughter = mom
        else:
            son = dad
            daughter = mom

        children.add_chromosome(Chromosome(son))
        children.add_chromosome(Chromosome(daughter))

    return children


def mutate(children: Population, pop_size: int,
           tm: float, net: Network) -> Population:
    """Custom mutation procedure based on DFS-like path creation

    Args:
        children: Chromosome offspring after crossover
        pop_size: number of individuals to compose the new population
        tm: mutation rate, which defines the percentage of individuals to
            undergo mutation
        net: Network instance

    Returns:
        Population: set of chromosomes to compose the new population

    """
    population = Population()
    while len(population) < pop_size:
        normal_chrom = np.random.choice(children.individuals)

        # DO NOT perform mutation if:
        # route has only one link which directly connects source to target
        # FIXME how the hell does it happen? It shouldn't ITFP.
        if len(normal_chrom) == 2:
            population.add_chromosome(normal_chrom)
            continue

        children.remove_chromosome_by_id(normal_chrom.id)

        trans_genes = list(normal_chrom.genes)

        if tm < np.random.random():
            # choose a random mutation point, excluding the first and the last
            geneid = np.random.randint(1, len(normal_chrom) - 1)

            # extract or pop() source and target nodes from chromosome
            start_router = trans_genes.pop(geneid)
            end_router = trans_genes.pop()

            # remove all genes after mutation point
            # FIXME no way this is right
            for gene in range(geneid, len(trans_genes)):
                trans_genes.pop()

            # alphabet: vertices that are not in genes before mutation point
            allels = {start_router, end_router}
            for node in range(net.nnodes):
                if node not in trans_genes:
                    allels.add(node)

            # create a new route R from mutation point to target node
            route = population.make_chromosome(net.a, start_router, end_router,
                                               allels, net.nnodes)

            # check if new route/path is valid
            if route is not None:
                trans_genes += route.genes
            else:
                trans_genes = list(normal_chrom.genes)

        population.add_chromosome(Chromosome(trans_genes))

    return population

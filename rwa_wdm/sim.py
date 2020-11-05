"""RWA simulator main function

"""

# [1] https://la.mathworks.com/matlabcentral/fileexchange/4797-wdm-network-blocking-computation-toolbox

import logging
from timeit import default_timer  # https://stackoverflow.com/a/25823885/3798300
from typing import Callable
from argparse import Namespace

import numpy as np

from .io import write_bp_to_disk, write_it_to_disk, plot_bp
from .net import Network

__all__ = (
    'get_net_instance_from_args',
    'get_rwa_algorithm_from_args',
    'simulator'
)

logger = logging.getLogger(__name__)


def get_net_instance_from_args(topname: str, numch: int) -> Network:
    """Instantiates a Network object from CLI string identifiers

    This is useful because rwa_wdm supports multiple network topology
    implementations, so this function acts like the instance is created
    directly.

    Args:
        topname: short identifier for the network topology
        numch: number of wavelength channels per network link

    Returns:
        Network: network topology instance

    Raises:
        ValueError: if `topname` is not a valid network identifier

    """
    if topname == 'nsf':
        from .net import NationalScienceFoundation
        return NationalScienceFoundation(numch)
    elif topname == 'clara':
        from .net import CooperacionLatinoAmericana
        return CooperacionLatinoAmericana(numch)
    elif topname == 'janet':
        from .net import JointAcademicNetwork
        return JointAcademicNetwork(numch)
    elif topname == 'rnp':
        from .net import RedeNacionalPesquisa
        return RedeNacionalPesquisa(numch)
    else:
        raise ValueError('No network named "%s"' % topname)


def get_rwa_algorithm_from_args(r_alg: str, wa_alg: str, rwa_alg: str,
                                ga_popsize: int, ga_ngen: int,
                                ga_xrate: float, ga_mrate: float) -> Callable:
    """Defines the main function to perform RWA from CLI string args

    Args:
        r_alg: identifier for a sole routing algorithm
        wa_alg: identifier for a sole wavelength assignment algorithm
        rwa_alg: identifier for a routine that performs RWA as one
        ga_popsize: population size for the GA-RWA procedure
        ga_ngen: number of generations for the GA-RWA procedure
        ga_xrate: crossover rate for the GA-RWA procedure
        ga_mrate: mutation rate for the GA-RWA procedure

    Returns:
        callable: a function that combines a routing algorithm and a
            wavelength assignment algorithm if those are provided
            separately, or an all-in-one RWA procedure
    
    Raises:
        ValueError: if neither `rwa_alg` nor both `r_alg` and `wa_alg`
            are provided

    """

    if r_alg is not None:  # NOTE implies `wa_alg` is not `None`
        if r_alg == 'dijkstra':
            if wa_alg == 'vertex-coloring':
                from .rwa import dijkstra_vertex_coloring
                return dijkstra_vertex_coloring
            elif wa_alg == 'first-fit':
                from .rwa import dijkstra_first_fit
                return dijkstra_first_fit
            else:
                raise ValueError('Unknown algorithm "%s"' % wa_alg)
        elif r_alg == 'yen':
            if wa_alg == 'vertex-coloring':
                from .rwa import yen_vertex_coloring
                return yen_vertex_coloring
            elif wa_alg == 'first-fit':
                from .rwa import yen_first_fit
                return yen_first_fit
            else:
                raise ValueError('Unknown algorithm "%s"' % wa_alg)
        else:
            raise ValueError('Unknown algorithm "%s"' % r_alg)
    elif rwa_alg is not None:
        if rwa_alg == 'genetic-algorithm':
            from .rwa import genetic_algorithm
            return genetic_algorithm(ga_popsize, ga_ngen, ga_xrate, ga_mrate)
        else:
            raise ValueError('Unknown algorithm "%s"' % rwa_alg)
    else:
        raise ValueError('Algorithm not specified')


def simulator(args: Namespace) -> None:
    """Main RWA simulation routine over WDM networks

    The loop levels of the simulator iterate over the number of repetitions,
    (simulations), the number of Erlangs (load), and the number of connection
    requests (calls) to be either allocated on the network or blocked if no
    resources happen to be available.

    Args:
        args: set of arguments provided via CLI to argparse module

    """

    # print header for pretty stdout console logging
    print('Load:   ', end='')
    for i in range(1, args.load + 1):
        print('%4d' % i, end=' ')
    print()

    time_per_simulation = []
    for simulation in range(args.num_sim):
        sim_time = default_timer()
        net = get_net_instance_from_args(args.topology, args.channels)
        rwa = get_rwa_algorithm_from_args(args.r, args.w, args.rwa,
                                          args.pop_size, args.num_gen,
                                          args.cross_rate, args.mut_rate)
        blocklist = []
        blocks_per_erlang = []

        # ascending loop through Erlangs
        for load in range(1, args.load + 1):
            blocks = 0
            for call in range(args.calls):
                print('\rBlocks: ', end='', flush=True)
                for b in blocklist:
                    print('%04d ' % b, end='', flush=True)
                print(' %04d' % call, end='')

                # Poisson arrival is modelled as an exponential distribution
                # of times, according to Pawełczak's MATLAB package [1]:
                # @until_next: time until the next call arrives
                # @holding_time: time an allocated call occupies net resources
                until_next = -np.log(1 - np.random.rand()) / load
                holding_time = -np.log(1 - np.random.rand())

                # Call RWA algorithm, which returns a lightpath if successful
                # or None if no λ can be found available at the route's first
                # link
                lightpath = rwa(net, args.y)

                # If lightpath is non None, the first link between the source
                # node and one of its neighbours has a wavelength available,
                # and the RWA algorithm running at that node thinks it can
                # allocate on that λ. However, we still need to check whether
                # that same wavelength is available on the remaining links
                # along the path in order to reach the destination node. In
                # other words, despite the RWA was successful at the first
                # node, the connection can still be blocked on further links
                # in the future hops to come, nevertheless.
                if lightpath is not None:
                    # check if the color chosen at the first link is available
                    # on all remaining links of the route
                    for (i, j) in lightpath.links:
                        if not net.n[i][j][lightpath.w]:
                            lightpath = None
                            break

                # Check if λ was not available either at the first link from
                # the source or at any other further link along the route.
                # Otherwise, allocate resources on the network for the
                # lightpath.
                if lightpath is None:
                    blocks += 1
                else:
                    lightpath.holding_time = holding_time
                    net.t.add_lightpath(lightpath)
                    for (i, j) in lightpath.links:
                        net.n[i][j][lightpath.w] = 0  # lock channel
                        net.t[i][j][lightpath.w] = holding_time

                        # make it symmetric
                        net.n[j][i][lightpath.w] = net.n[i][j][lightpath.w]
                        net.t[j][i][lightpath.w] = net.t[i][j][lightpath.w]

                # FIXME The following two routines below are part of the same
                # one: decreasing the time network resources remain allocated
                # to connections, and removing finished connections from the
                # traffic matrix. This, however, should be a single routine
                # iterating over lightpaths links instead of all edges, so when
                # the time is up on all links of a lightpath, the lightpath
                # might be popped from the matrix's list. I guess the problem
                # is the random initialisation of the traffic matrix's holding
                # times during network object instantiation, but if this is
                # indeed the fact it needs some consistent testing.
                for lightpath in net.t.lightpaths:
                    if lightpath.holding_time > until_next:
                        lightpath.holding_time -= until_next
                    else:
                        # time's up: remove conn from traffic matrix's list
                        net.t.remove_lightpath_by_id(lightpath.id)

                # Update *all* channels that are still in use
                for (i, j) in net.get_edges():
                    for w in range(net.nchannels):
                        if net.t[i][j][w] > until_next:
                            net.t[i][j][w] -= until_next
                        else:
                            # time's up: free channel
                            net.t[i][j][w] = 0
                            if not net.n[i][j][w]:
                                net.n[i][j][w] = 1  # free channel

                        # make matrices symmetric
                        net.t[j][i][w] = net.t[i][j][w]
                        net.n[j][i][w] = net.n[j][i][w]

            blocklist.append(blocks)
            blocks_per_erlang.append(100.0 * blocks / args.calls)

        sim_time = default_timer() - sim_time
        time_per_simulation.append(sim_time)

        print('\rBlocks: ', end='', flush=True)
        for b in blocklist:
            print('%04d ' % b, end='', flush=True)
        print('\n%-7s ' % 'BP (%):', end='')
        print(' '.join(['%4.1f' % b for b in blocks_per_erlang]), end=' ')
        print('[sim %d: %.2f secs]' % (simulation + 1, sim_time))

        fbase = '%s_%dch_%dreq_%s' % (
            args.rwa if args.rwa is not None else '%s_%s' % (args.r, args.w),
            args.channels, args.calls, net.name)

        write_bp_to_disk(args.result_dir, fbase + '.bp', blocks_per_erlang)

    write_it_to_disk(args.result_dir, fbase + '.it', time_per_simulation)

    if args.plot:
        plot_bp(args.result_dir)

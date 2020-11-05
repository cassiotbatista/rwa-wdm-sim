# PYTHON_ARGCOMPLETE_OK
"""Enable the execution of "rwa_wdm" package as a command line program with the
``-m`` switch. For example:

.. code-block:: sh

    python -m rwa_wdm -t janet -r dijkstra -w vertex-coloring -s 10 -p

"""
import os
import logging
import argcomplete
import argparse
import tempfile

from . import simulator
from .util import validate_args

logger = logging.getLogger(__name__)
TEMP_DIR = os.path.join(tempfile.gettempdir(), 'rwa_results')


fmt = lambda prog: argparse.ArgumentDefaultsHelpFormatter(
    "python -m rwa_wdm", width=220, max_help_position=250)
parser = argparse.ArgumentParser(
    formatter_class=fmt,
    description='RWA WDM Simulator: routing and wavelength assignment '
                'simulator for WDM networks',
    usage='%(prog)s [-h] [-r <alg> -w <alg> | --rwa <alg>] [options]')

net = parser.add_argument_group('Network options')
rwa = parser.add_argument_group('RWA algorithms options')
sim = parser.add_argument_group('RWA simulator options')
ga = parser.add_argument_group('Genetic algorithm options')

# network topology options
net.add_argument('-t', default='nsf', dest='topology',
                 choices=['nsf', 'clara', 'janet', 'rnp'],
                 metavar='<topology>',
                 help='network topology')
net.add_argument('-c', type=int, default=8, dest='channels',
                 choices=[2 ** (i + 1) for i in range(8)],  # max: 256
                 metavar='<channels>',
                 help='number of λ per link')

# rwa algorithms options
# TODO [ -r <algorithms> -w <algorithm> ] [ --rwa <algorithm> ]
# https://stackoverflow.com/questions/17909294/python-argparse-mutual-exclusive-group
rwa.add_argument('-r', metavar='<algorithm>',
                 choices=['dijkstra', 'yen'],
                 help='routing algorithm')
rwa.add_argument('-w', metavar='<algorithm>',
                 choices=['vertex-coloring', 'first-fit'],
                 help='wavelength assignment algorithm')
rwa.add_argument('--rwa', metavar='<algorithm>',
                 choices=['genetic-algorithm'],
                 help='routing *and* wavelength assigment algorithm')
rwa.add_argument('-y', metavar='<yen-alt-paths>', type=int,
                 default=2, choices=range(2, 5),
                 help='number of routing alternate paths (Yen\'s)')

# simulation options
sim.add_argument('-l', type=int, default=30, dest='load',
                 metavar='<max-load>', choices=range(10, 256),
                 help='maximum network load, in Erlangs')
sim.add_argument('-k', type=int, default=150, dest='calls',
                 metavar='<conn-requests>',
                 help='number of connection requests to arrive')
sim.add_argument('-d', default=TEMP_DIR, dest='result_dir',
                 metavar='<result-dir>',
                 help='dir to store blocking probability results')
sim.add_argument('-s', type=int, default=1, dest='num_sim',
                 metavar='<num-simulations>',
                 help='number of times to run the simulation')
sim.add_argument('-p', default=False, dest='plot', action='store_true',
                 help='plot blocking probability graph after simulation?')

# genetic algorithm options
ga.add_argument('--pop-size', type=int, default=25,
                help='number of individuals in the population')
ga.add_argument('--num-gen', type=int, default=25,
                help='number of generations for population to evolve')
ga.add_argument('--cross-rate', type=float, default=0.40,
                help='crossover rate')
ga.add_argument('--mut-rate', type=float, default=0.02,
                help='mutation rate')

# FIXME this ain't working on my machine and I have no clue why
argcomplete.autocomplete(parser)
argcomplete.autocomplete(net)
argcomplete.autocomplete(rwa)
argcomplete.autocomplete(sim)
argcomplete.autocomplete(ga)

if __name__ == '__main__':
    args = parser.parse_args()
    try:
        validate_args(args)
    except ValueError as e:
        logger.error('Bad input: %s', e)
    else:
        logger.info('Simulating %s connection requests over %s topology with '
                    '%d λ per link using %s as RWA algorithm' %
                    (args.calls, args.topology, args.channels,
                     args.rwa if args.rwa is not None else
                     '%s + %s combination' % (args.r, args.w)))
        simulator(args)

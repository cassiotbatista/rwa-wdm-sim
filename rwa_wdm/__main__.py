import logging
import argparse

from .sim import rwa_simulator

logger = logging.getLogger(__name__)


if __name__ == '__main__':
    fmt = lambda prog: argparse.HelpFormatter("python -m rwa_wdm", width=220,
                                              max_help_position=250)
    parser = argparse.ArgumentParser(
        formatter_class=fmt, description='RWA simulator for WDM networks')

    net = parser.add_argument_group('network')
    rwa = parser.add_argument_group('rwa-algorithms')
    sim = parser.add_argument_group('simulator')

    # network topology options
    net.add_argument('-t', default='nsf', dest='topology',
                     choices=['nsf', 'clara', 'janet', 'rnp'],
                     metavar='<topology>',
                     help='network topology')
    net.add_argument('-c', type=int, default=8, dest='channels',
                     choices=[2 ** (i + 1) for i in range(8)],  # max: 256
                     metavar='<channels>',
                     help='number of wavelength channels (λ) per link')

    # rwa algorithms options
    # TODO https://stackoverflow.com/questions/17909294/python-argparse-mutual-exclusive-group
    rwa.add_argument('-r', metavar='<algorithm>',
                     choices=['dijkstra', 'yen'],
                     help='routing algorithm')
    rwa.add_argument('-w', metavar='<algorithm>',
                     choices=['vertex-coloring', 'first-fit'],
                     help='wavelength assignment algorithm')
    rwa.add_argument('--rwa-alg', metavar='<algorithm>', choices=['ga'],
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
    sim.add_argument('-d', default='results', dest='result_dir',
                     metavar='<result-dir>',
                     help='dir to store blocking probability calculations')
    sim.add_argument('-p', default=False, dest='plot', action='store_true',
                     help='plot blocking probability graph after simulation?')

    args = parser.parse_args()

    # summary
    logging.info('Simulating over %s topology with %d channels using '
                 'algorithms (%s + %s | %s)' % (args.topology, args.channels,
                                                args.r, args.w, args.rwa_alg))

    rwa_simulator(args)

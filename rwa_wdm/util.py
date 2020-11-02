import logging
from argparse import Namespace

logger = logging.getLogger(__name__)


class Args(Namespace):
    pass


def validate_args(args: Namespace) -> None:

    if args.rwa_alg is None:
        if args.r_alg is None and args.w_alg is None:
            raise ValueError('The use of either --rwa flag or both -r and -w '
                             'combined is required.')
        elif not (args.r_alg and args.w_alg):
            raise ValueError('Flags -r and -w should be set in combination.')
    elif args.rwa_alg is not None:
        if args.r_alg is not None or args.w_alg is not None:
            raise ValueError('Set either --rwa flag alone or both -r and -w '
                             'flags combined.')
    if args.y is not None:
        if args.r_alg != 'yen':
            logger.warning('Alternate paths will not take effect if Yen\'s '
                           'algorithm is not chosen for routing.')

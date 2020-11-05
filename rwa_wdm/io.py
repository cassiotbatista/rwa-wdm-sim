"""I/O related operations such as R/W data from disk and viz-related ops

"""

import os
import glob
import logging
from typing import List

import numpy as np
import matplotlib.pyplot as plt

__all__ = ('write_bp_to_disk', 'write_it_to_disk', 'plot_bp')

logger = logging.getLogger(__name__)


def write_bp_to_disk(result_dir: str,
                     filename: str, bplist: List[float]) -> None:
    """Writes blocking probabilities to text file

    Args:
        result_dir: directory to write files to
        filename: name of the file to be written
        itlist: list of blocking probability values, as percentages, to be
            dumped to file

    """
    if not os.path.isdir(result_dir):
        logger.info('Creating result dir in %s' % result_dir)
        os.mkdir(result_dir)

    filepath = os.path.join(result_dir, filename)
    logger.info('Writing blocking probability results to file "%s"' % filepath)
    with open(filepath, 'a') as f:
        for bp in bplist:
            f.write(' %7.3f' % bp)
        f.write('\n')


def write_it_to_disk(result_dir: str,
                     filename: str, itlist: List[float]) -> None:
    """Writes profiling time information to text file

    Args:
        result_dir: directory to write files to
        filename: name of the file to be written
        itlist: list of times, in seconds, to be dumped to file

    """
    if not os.path.isdir(result_dir):
        logger.info('Creating result dir in %s' % result_dir)
        os.mkdir(result_dir)

    filepath = os.path.join(result_dir, filename)
    logger.info('Writing simulation profiling times to file "%s"' % filepath)
    with open(filepath, 'a') as f:
        for it in itlist:
            f.write(' %7.7f' % it)


def plot_bp(result_dir: str) -> None:
    """Reads blocking probabilities from file and plot overlapping graph

    Args:
        result_dir: directory that stores files to be read

    """
    filelist = []
    for f in glob.glob(os.path.join(result_dir, '*.bp')):
        filelist.append(os.path.basename(f))
        data = np.loadtxt(f)
        if data.ndim == 1:
            max_load =  data.shape[0] + 1
            plt.plot(np.arange(1, max_load), data, '--')
        else:
            max_load =  data.shape[1] + 1
            plt.plot(np.arange(1, max_load), data.mean(axis=0), '--')
        plt.xlim(0.5, max_load - 0.5)
        if data.ndim == 1 or data.shape[0] < 10:
            logger.warning('Remember you should simulate at least 10 times '
                           '(found only %d in %s)' % (data.shape[0], f))
    plt.grid()
    plt.ylabel('Blocking probability (%)', fontsize=18)
    plt.xlabel('Load (Erlangs)', fontsize=18)
    plt.title('Average mean blocking probability', fontsize=20)
    plt.legend(filelist)
    plt.show(block=True)

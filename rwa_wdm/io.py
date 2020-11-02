"""I/O related operations such as R/W data from disk and viz-related ops

"""

import os
import glob
import logging

import numpy as np
import matplotlib.pyplot as plt

logger = logging.getLogger(__name__)  # noqa


def write_results_to_disk(result_dir, filename, bplist):
    """Write blocking probabilities to text file

    """
    if not os.path.isdir(result_dir):
        logger.info('Creating result dir in %s' % result_dir)
        os.mkdir(result_dir)

    filepath = os.path.join(result_dir, filename)
    logger.info('Writing results to file "%s"' % filepath)
    with open(filepath, 'a') as f:
        for bp in bplist:
            f.write(' %7.3f' % bp)
        f.write('\n')


def plot_blocking_probability(result_dir):
    """Reads blocking probabilities from file and plot overlapping graph

    """
    filelist = []
    for f in glob.glob(os.path.join(result_dir, '*.bp')):
        filelist.append(os.path.basename(f))
        data = np.loadtxt(f)
        if data.ndim == 1:
            plt.plot(data, '--')
        else:
            plt.plot(data.mean(axis=0), '--')
        if data.ndim == 1 or data.shape[0] < 10:
            logger.warning('Remember you should simulate at least 10 times '
                           '(found only %d in %s)' % (data.shape[0], f))
    plt.grid()
    plt.ylabel('Blocking probability (%)', fontsize=18)
    plt.xlabel('Load (Erlangs)', fontsize=18)
    plt.title('Average mean blocking probability', fontsize=20)
    plt.legend(filelist)
    plt.show(block=True)

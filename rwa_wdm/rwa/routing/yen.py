"""Yen's algorithm, a.k.a. k-shortest paths algorithm as routing strategy

"""

from typing import List

import numpy as np
import networkx as nx


def yen(mat: np.ndarray, s: int, d: int, k: int) -> List[List[int]]:
    """Yen's routing algorithm, a.k.a. K-shortest paths

    Args:
        mat: Network's adjacency matrix graph
        s: source node index
        d: destination node index
        k: number of alternate paths

    Returns:
        :obj:`list` of :obj:`list`: a sequence of `k` paths

    """
    if s < 0 or d < 0:
        raise ValueError('Source nor destination nodes cannot be negative')
    elif s > mat.shape[0] or d > mat.shape[0]:
        raise ValueError('Source nor destination nodes should exceed '
                         'adjacency matrix dimensions')
    if k < 0:
        raise ValueError('Number of alternate paths should be positive')

    G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
    paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
    return paths[:k]

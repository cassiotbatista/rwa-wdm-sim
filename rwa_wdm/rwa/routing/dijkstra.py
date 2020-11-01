"""Dijkstra shortest path algorithm as routing strategy

"""

from typing import List

import numpy as np
import networkx as nx


def dijkstra(mat: np.ndarray, s: int, d: int) -> List[int]:
    """Dijkstra routing algorithm

    """
    if s < 0 or d < 0:
        raise ValueError('Source nor destination nodes cannot be negative')
    elif s > mat.shape[0] or d > mat.shape[0]:
        raise ValueError('Source nor destination nodes should exceed '
                         'adjacency matrix dimentions')

    G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
    hops, path = nx.bidirectional_dijkstra(G, s, d, weight=None)
    return path

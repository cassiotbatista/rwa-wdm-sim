from typing import List

import numpy as np
import networkx as nx


def lora(mat: np.ndarray, s: int, d: int, k: int) -> List[List[int]]:
    """Lexicographical Routing Algorithm (LORA)

    Args:
        mat: Network's adjacency matrix graph
        s: source node index
        d: destination node index
        k: number of alternate paths

    Returns:
        :obj:`list` of :obj:`list`: a sequence of `k` paths in lexicographical order

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
    paths = sorted(paths)[:k]  # Sort paths lexicographically and select first k paths

    return paths

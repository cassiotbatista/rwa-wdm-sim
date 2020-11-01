from itertools import count
from typing import List, Union

import numpy as np
import networkx as nx

# FIXME https://mypy.readthedocs.io/en/latest/common_issues.html#import-cycles
from rwa_wdm.net import Network, Lightpath


def greedy_color(H, colors):
    """Vertex coloring strategy

    """
    G = nx.from_numpy_matrix(H, create_using=nx.Graph())

    if len(G):
        u = H.shape[0] - 1
        neighbour_colors = {colors[v] for v in G[u] if v in colors}
        for color in count():
            if color not in neighbour_colors:
                break

        # assign the node the newly found color
        return color


def vertex_coloring(net: Network, lightpath: Lightpath) -> Union[int, None]:
    """Vertex coloring algorithm

    """
    net.t.add_lightpath(lightpath)  # this is temporary

    # NOTE `num_conns` gotta be at least one for this to work. The current
    # route is assumed to be already in the graph when vertex coloring
    # strategies take place, because the route we are trying to find a λ to
    # must be already accounted for as part of the "group" of routes.
    H = np.zeros((net.t.num_conns, net.t.num_conns), dtype=np.uint16)
    if net.t.num_conns > 1:
        # cross compare paths over indices i and j
        for i in range(net.t.num_conns):
            for j in range(i + 1, net.t.num_conns):
                r1 = net.t.lightpaths[i].r
                r2 = net.t.lightpaths[j].r
                # cross compare routers over indicies m and n
                for m in range(1, len(r1)):
                    for n in range(1, len(r2)):
                        if (r1[m - 1] == r2[n - 1] and r1[m] == r2[n]) or \
                           (r1[m] == r2[n - 1] and r1[m - 1] == r2[n]):
                            H[i][j] = 1
                            H[j][i] = 1

    colors = {}
    for i in range(net.t.num_conns):
        wavelength = net.t.lightpaths[i].w
        if wavelength is not None:
            colors[i] = wavelength

    net.t.remove_lightpath_by_id(lightpath.id)  # I told you it was temporary

    return greedy_color(H, colors)

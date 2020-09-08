#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA with Fixed Alternate Path + Greedy Coloring
# Routing with Dijkstra -> 1-shortest path
# Wavelength Assignment with Sequential Vertex Coloring and Largest-First Ordering
#
# Copyright 2017 Universidade Federal do Pará (PPGCC UFPA)
#
# Authors: Jan 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com

# Last revised on June 2020

# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks


import itertools
import numpy as np
import networkx as nx

from net import nsf as net
import info


# https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.shortest_paths.html
def dijkstra(mat, s, d):
    if any([s,d])<0 or any([s,d])>mat.shape[0]:
        print('Error')
        return None, None
    G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
    hops, path = nx.bidirectional_dijkstra(G, s, d, weight=None)
    return path

# https://networkx.github.io/documentation/development/_modules/networkx/algorithms/coloring/greedy_coloring.html
# https://networkx.github.io/documentation/development/reference/algorithms.coloring.html
def greedy_color(H, colors, strategy=nx.coloring.strategy_largest_first):
    G = nx.from_numpy_matrix(H, create_using=nx.Graph())

    if len(G):
        # set to keep track of colors of neighbours
        neighbour_colors = set()

        #node = G.nodes()[-1] # last node added
        #for neighbour in G.neighbors_iter(node):
        #    if neighbour in colors:
        #        neighbour_colors.add(colors[neighbour])

        u = H.shape[0]-1
        neighbour_colors = {colors[v] for v in G[u] if v in colors}
        for color in itertools.count():
            if color not in neighbour_colors:
                break

        # assign the node the newly found color
        #colors[node] = color
        return color

    #return colors

def get_wave_availability(k, n):
    return (int(n) & ( 1 << k )) >> k

def rwa_std_fix(N, A, T, holding_time, paths):
    R = dijkstra(A, net.SOURCE_NODE, net.DEST_NODE)
    paths.append([R, None])

    H = np.zeros((len(paths), len(paths)), dtype=np.int)
    if len(paths) > 1:
        for i in range(len(paths)): # cross compare paths on i and j
            for j in range(i+1, len(paths)):
                for m in range(1,len(paths[i][0])): # cross compare routers on m and n
                    for n in range(1,len(paths[j][0])):
                        if (paths[i][0][m-1] == paths[j][0][n-1] and \
                            paths[i][0][m]   == paths[j][0][n]) \
                            or \
                            (paths[i][0][m]  == paths[j][0][n-1] and \
                            paths[i][0][m-1] == paths[j][0][n]):
                            H[i][j] = 1
                            H[j][i] = 1

    colors = {}
    for i in range(len(paths)):
        if paths[i][1] is not None:
            colors[i] = paths[i][1]

    color = greedy_color(H, colors)

    if color < info.NUM_CHANNELS:
        for r in range(len(R)-1):
            rcurr = R[r]
            rnext = R[r+1]

            if not get_wave_availability(color, N[rcurr][rnext]):
                color = None
                break
    else:
        color = None

    # update NSF graph
    if color is not None:
        for r in range(len(R)-1):
            rcurr = R[r]
            rnext = R[r+1]

            N[rcurr][rnext] -= 2**color
            N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric

            T[rcurr][rnext][color] = holding_time
            T[rnext][rcurr][color] = T[rcurr][rnext][color]

        paths[-1][1] = color  # update color of the last route
        return 0 # allocated
    else:
        paths.pop(-1)
        return 1 # blocked

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm
# Routing and Wavelength Assignment
# General Objective Function
#
# Copyright 2020
# Programa de Pós-Graduação em Ciência da Computação (PPGCC)
# Universidade Federal do Pará (UFPA)
#
# Author: September 2020
# Cassio Trindade Batista - cassio.batista.13@gmail.com
#
# Last revised on September 2020


import random
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.ticker import EngFormatter

import info

SOURCE_NODE  = 1     # source for all cals
DEST_NODE    = 6     # destination node
NUM_NODES    = 7     # number of nodes on CLARA network


def generate():
    def set_wave_availability():
        nwaves = 2**info.NUM_CHANNELS
        if info.CHANNEL_FREE:
            return np.uint8(nwaves-1)
        return np.uint8(random.randrange(1, nwaves))

    # define links or edges as node index pairs 
    nsf_links = [\
            (0,1), (0,2),                # 0
            (1,2), (1,3),                # 1
            (2,4),                       # 2
            (3,4), (3,5), #(3,6),        # 3
            (4,6),                       # 4
            (5,6)                        # 5
    ]

    nsf_wave = np.zeros((NUM_NODES, NUM_NODES), dtype=np.uint8)
    for link in nsf_links:
        nsf_wave[link[0]][link[1]] = set_wave_availability() 
        nsf_wave[link[1]][link[0]] = nsf_wave[link[0]][link[1]]

    nsf_adj = np.zeros((NUM_NODES, NUM_NODES), dtype=np.uint8)
    for link in nsf_links:
        nsf_adj[link[0]][link[1]] = 1
        nsf_adj[link[1]][link[0]] = nsf_adj[link[0]][link[1]] 

    nsf_time = np.zeros((NUM_NODES, NUM_NODES, info.NUM_CHANNELS))
    for link in nsf_links:
        availability = format(nsf_wave[link[0]][link[1]], '0%db' % info.NUM_CHANNELS)
        for w in range(info.NUM_CHANNELS):
            nsf_time[link[0]][link[1]][w] = int(availability[w]) * np.random.rand()
            nsf_time[link[1]][link[0]][w] = nsf_time[link[0]][link[1]][w]

    return nsf_wave, nsf_adj, nsf_time, nsf_links

def plot_graph(bestroute=False):
    fig = plt.figure()
    ax = fig.add_subplot(111)

    # define vertices or nodes as points in 2D cartesian plan
    nsfnodes = [\
            ['Gla', (1.50, 4.00)], # 0
            ['Man', (1.00, 3.00)], # 1
            ['Lee', (2.00, 3.00)], # 2
            ['Bir', (1.00, 2.00)], # 3
            ['Not', (2.00, 2.00)], # 4
            ['Bri', (1.00, 1.00)], # 5
            ['Lon', (2.00, 1.00)]  # 6
    ]

    # define links or edges as node index ordered pairs in cartesian plan
    nsf_links = [\
            (0,1), (0,2),                # 0
            (1,2), (1,3),                # 1
            (2,4),                       # 2
            (3,4), (3,5), #(3,6),        # 3
            (4,6),                       # 4
            (5,6)                        # 5
    ]

    # grid
    ax.grid()

    # draw edges before vertices
    for link in nsf_links:
        x = [ nsfnodes[link[0]][1][0], nsfnodes[link[1]][1][0] ]
        y = [ nsfnodes[link[0]][1][1], nsfnodes[link[1]][1][1] ]
        plt.plot(x, y, 'k', linewidth=2)

    # highlight in red the shortest path with wavelength(s) available
    if bestroute:
        for i in range(len(bestroute)-1):
            x = [ nsfnodes[bestroute[i]][0], nsfnodes[bestroute[i+1]][0] ]
            y = [ nsfnodes[bestroute[i]][1], nsfnodes[bestroute[i+1]][1] ]
            plt.plot(x, y, 'r', linewidth=2.5)

    # draw vertices
    i = 0
    for node in nsfnodes:
        # parameter to adjust text on the center of the vertice
        if i < 10:
            corr = 0.060
        else:
            corr = 0.085

        plt.plot(node[1][0], node[1][1], 'wo', ms=25, mec='k')

        # write node index on the center of the node
        ax.annotate(node[0], xy=(node[1][0]-corr, node[1][1]-corr))
        i += 1

    plt.xticks(np.arange(0, 4, 1))
    plt.yticks(np.arange(0, 6, 1))
    plt.show(block=True)

if __name__ == '__main__':
    plot_graph()

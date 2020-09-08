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

SOURCE_NODE  = 3      # source for all cals
DEST_NODE    = 11      # destination node
NUM_NODES    = 28     # number of nodes on CLARA network


def generate():
    def set_wave_availability():
        nwaves = 2**info.NUM_CHANNELS
        if info.CHANNEL_FREE:
            return np.uint8(nwaves-1)
        return np.uint8(random.randrange(1, nwaves))

    # define links or edges as node index pairs 
    nsf_links = [\
            (0,1),                                #  0
            (1,3), (1,4),                         #  1
            (2,4),                                #  2
            (3,4), (3,7), (3,17), (3,19), (3,25), #  3
            (4,6), (4,12),                        #  4
            (5,25),                               #  5
            (6,7),                                #  6
            (7,8), (7,11), (7,18), (7,19),        #  7
            (8,9),                                #  8
            (9,10),                               #  9
            (10,11),                              # 10
            (11,12), (11,13), (11,15),            # 11
            (13,14),                              # 13
            (14,15),                              # 14
            (15,16), (15,19),                     # 15
            (16,17),                              # 16
            (17,18),                              # 17
            (18,19), (18,20), (18,22),            # 18
            (20,21),                              # 20
            (21,22),                              # 21
            (22,23),                              # 22
            (23,24),                              # 23
            (24,25), (24,26),                     # 24
            (26,27)                               # 26
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
            ['RR', (5.00,  3.25)], #  0
            ['AM', (5.50,  3.75)], #  1
            ['AP', (8.25,  3.75)], #  2
            ['DF', (4.00,  5.00)], #  3
            ['PA', (9.00,  3.00)], #  4
            ['TO', (3.00,  3.00)], #  5
            ['MA', (9.00,  4.00)], #  6
            ['CE', (9.50,  5.00)], #  7
            ['RN', (10.50, 5.00)], #  8
            ['PB', (10.50, 3.00)], #  9
            ['PB', (10.50, 1.00)], # 10
            ['PE', (9.50,  1.00)], # 11
            ['PI', (9.00,  2.00)], # 12
            ['AL', (8.00,  2.00)], # 13
            ['SE', (7.00,  2.00)], # 14
            ['BA', (6.00,  2.00)], # 15
            ['ES', (6.00,  1.00)], # 16
            ['RJ', (4.00,  1.00)], # 17
            ['SP', (2.00,  1.00)], # 18
            ['MG', (6.00,  5.50)], # 19
            ['SC', (1.00,  1.00)], # 20
            ['RS', (1.00,  2.00)], # 21
            ['PR', (2.00,  2.00)], # 22
            ['MS', (2.00,  4.00)], # 23
            ['MT', (2.00,  5.00)], # 24
            ['GO', (3.00,  5.00)], # 25
            ['RO', (1.00,  5.00)], # 26
            ['AC', (1.00,  4.00)]  # 27
    ]

    # define links or edges as node index ordered pairs in cartesian plan
    nsf_links = [\
            (0,1),                                #  0
            (1,3), (1,4),                         #  1
            (2,4),                                #  2
            (3,4), (3,7), (3,17), (3,19), (3,25), #  3
            (4,6), (4,12),                        #  4
            (5,25),                               #  5
            (6,7),                                #  6
            (7,8), (7,11), (7,18), (7,19),        #  7
            (8,9),                                #  8
            (9,10),                               #  9
            (10,11),                              # 10
            (11,12), (11,13), (11,15),            # 11
            (13,14),                              # 13
            (14,15),                              # 14
            (15,16), (15,19),                     # 15
            (16,17),                              # 16
            (17,18),                              # 17
            (18,19), (18,20), (18,22),            # 18
            (20,21),                              # 20
            (21,22),                              # 21
            (22,23),                              # 22
            (23,24),                              # 23
            (24,25), (24,26),                     # 24
            (26,27)                               # 26
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

    plt.xticks(np.arange(0, 12, 1))
    plt.yticks(np.arange(0, 7, 1))
    plt.show(block=True)

if __name__ == '__main__':
    plot_graph()

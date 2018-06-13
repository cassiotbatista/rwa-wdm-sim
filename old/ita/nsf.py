#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm
# Routing and Wavelength Assignment
# General Objective Function
#
# Copyright 2017
# Programa de Pós-Graduação em Ciência da Computação (PPGCC)
# Universidade Federal do Pará (UFPA)
#
# Author: April 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
#
# Last revised on February 2017


import sys
reload(sys)  
sys.setdefaultencoding('utf8') # for plot in PT_BR

import info
import random
import numpy as np

import matplotlib.pyplot as plt
import matplotlib.animation as anim
from matplotlib.ticker import EngFormatter


def generate():
	def set_wave_availability():
		nwaves = 2**info.NSF_NUM_CHANNELS
		if info.NSF_CHANNEL_FREE:
			return np.uint8(nwaves-1)
		return np.uint8(random.randrange(1, nwaves))

	# define links or edges as node index pairs 
	nsf_links = [\
		(0,1), (0,2), (0,5),  # 0
		(1,2), (1,3),         # 1
		(2,8),                # 2
		(3,4), (3,6), (3,13), # 3
		(4,9),                # 4
		(5,6), (5,10),        # 5
		(6,7),                # 6
		(7,8),                # 7
		(8,9),                # 8
		(9,11), (9,12),       # 9
		(10,11), (10,12),     # 10
		(11,13)               # 11
	]

	nsf_wave = np.zeros((info.NSF_NUM_NODES, info.NSF_NUM_NODES), dtype=np.uint8)
	for link in nsf_links:
		nsf_wave[link[0]][link[1]] = set_wave_availability() 
		nsf_wave[link[1]][link[0]] = nsf_wave[link[0]][link[1]] 

	nsf_adj = np.zeros((info.NSF_NUM_NODES, info.NSF_NUM_NODES), dtype=np.uint8)
	for link in nsf_links:
		nsf_adj[link[0]][link[1]] = 1
		nsf_adj[link[1]][link[0]] = nsf_adj[link[0]][link[1]] 

	nsf_time = np.zeros((info.NSF_NUM_NODES, info.NSF_NUM_NODES, info.NSF_NUM_CHANNELS))
	for link in nsf_links:
		availability = format(nsf_wave[link[0]][link[1]], '0%db' % info.NSF_NUM_CHANNELS)
		for w in xrange(info.NSF_NUM_CHANNELS):
			nsf_time[link[0]][link[1]][w] = int(availability[w]) * np.random.rand()
			nsf_time[link[1]][link[0]][w] = nsf_time[link[0]][link[1]][w]

	return nsf_wave, nsf_adj, nsf_time, nsf_links

### EOF ###

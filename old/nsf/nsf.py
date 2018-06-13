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

def plot_fits(fits):
	plt.interactive(True) # don't interrupt program flow to plot
	fig, ax = plt.subplots()
	ax.set_xscale('linear')
	formatter = EngFormatter(unit='', places=1)
	ax.xaxis.set_major_formatter(formatter)
	ax.set_xlabel(u'Gerações', fontsize=20)
	ax.set_ylabel(u'Número de chamadas atendidas', fontsize=20)

	ax.grid()
	ax.plot(fits, linewidth=2.0)

	x = range(0, info.GA_MAX_GEN, 5)
	y = np.arange(0, 8, 1)

	fig.suptitle(u'Melhores Fits de %d Indivíduos por Geração'\
				% info.GA_SIZE_POP, fontsize=20)
	#plt.margins(0.02)
	plt.subplots_adjust(bottom=0.12)

	#plt.xticks(x)
	plt.yticks(y)
	plt.draw()
	plt.show(block=True)


def plot_graph(bestroute=False):
	fig = plt.figure()
	ax = fig.add_subplot(111)

	# define vertices or nodes as points in 2D cartesian plan
	nsfnodes = [\
		(0.70, 2.70), # 0
		(1.20, 1.70), # 1
		(1.00, 4.00), # 2
		(3.10, 1.00), # 3
		(4.90, 0.70), # 4
		(2.00, 2.74), # 5
		(2.90, 2.66), # 6
		(3.70, 2.80), # 7
		(4.60, 2.80), # 8
		(5.80, 3.10), # 9
		(5.50, 3.90), # 10
		(6.60, 4.60), # 11
		(7.40, 3.30), # 12
		(6.50, 2.40), # 13
	]

	# define links or edges as node index ordered pairs in cartesian plan
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

	# grid
	ax.grid()

	# draw edges before vertices
	for link in nsf_links:
		x = [ nsfnodes[link[0]][0], nsfnodes[link[1]][0] ]
		y = [ nsfnodes[link[0]][1], nsfnodes[link[1]][1] ]
		plt.plot(x, y, 'k', linewidth=2)

	# highlight in red the shortest path with wavelength(s) available
	if bestroute:
		for i in xrange(len(bestroute)-1):
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

		plt.plot(node[0], node[1], 'wo', markersize=25)

		# write node index on the center of the node
		ax.annotate(str(i), xy=(node[0]-corr, node[1]-corr))
		i += 1
	
	plt.xticks(np.arange(0, 9, 1))
	plt.yticks(np.arange(0, 7, 1))
	plt.show(block=True)

#def nsfnet_generator_recover():
#''.join( [random.choice((0,1)) for i in xrange(info.NSF_NUM_NODES)] )

### EOF ###

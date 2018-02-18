#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA with Fixed Alternate Path + Greedy Coloring
# Routing with Yen -> k-shortest path
# Wavelength Assignment with Sequential Vertex Coloring and Largest-First Ordering
#
# Authors: Jan 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last revised on Apr 2017
#
# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks


import info

import itertools
import numpy as np
import networkx as nx

# https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.simple_paths.html
def yen(mat, (s,d), k):
	if any([s,d])<0 or any([s,d])>mat.shape[0] or k<0:
		print 'Error'
		return None
	G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
	paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
	return paths[:k]

# https://networkx.github.io/documentation/development/_modules/networkx/algorithms/coloring/greedy_coloring.html
# https://networkx.github.io/documentation/development/reference/algorithms.coloring.html
def greedy_color(H, colors, strategy=nx.coloring.strategy_largest_first):
	G = nx.from_numpy_matrix(H, create_using=nx.Graph())

	if len(G):
		# set to keep track of colors of neighbours
		neighbour_colors = set()

		node = G.nodes()[-1] # last node added

		for neighbour in G.neighbors_iter(node):
			if neighbour in colors:
				neighbour_colors.add(colors[neighbour])

		for color in itertools.count():
			if color not in neighbour_colors:
				break

		return color

def get_wave_availability(k, n):
	return (int(n) & ( 1 << k )) >> k

def rwa_std_alt(N, A, T, holding_time, paths):
	SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)

	routes = yen(A, SD, info.K)

	for R in routes:
		paths.append([R, None])

		H = np.zeros((len(paths), len(paths)), dtype=np.int)
		if len(paths) > 1:
			for i in xrange(len(paths)): # cross compare paths on i and j
				for j in xrange(i+1, len(paths)):
					for m in xrange(1,len(paths[i][0])): # cross compare routers on m and n
						for n in xrange(1,len(paths[j][0])):
							if (paths[i][0][m-1] == paths[j][0][n-1] and \
								paths[i][0][m]   == paths[j][0][n]) \
								or \
								(paths[i][0][m]  == paths[j][0][n-1] and \
								paths[i][0][m-1] == paths[j][0][n]):
								H[i][j] = 1
								H[j][i] = 1

		colors = {}
		for i in xrange(len(paths)):
			if paths[i][1] is not None:
				colors[i] = paths[i][1]

		color = greedy_color(H, colors)

		if color < info.NSF_NUM_CHANNELS:
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				if not get_wave_availability(color, N[rcurr][rnext]):
					color = None
					break
		else:
			color = None

		# update NSF graph
		if color is not None:
			for r in xrange(len(R)-1):
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
			# try another route insted of blocking immediately

	return 1 # blocked

### EOF ###

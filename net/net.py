#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm
# Routing and Wavelength Assignment
# General Objective Function
#
# Author: Feb 2018
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# First version: Apr 2016
# Last edited on Feb 2018
#
# References:
# - random 'biased' choice: https://stackoverflow.com/q/25507558

import random
import numpy as np

class Network:
	""" Network: A superclass that does something """
	WAVELENGTH_MATRIX = None   # N (3D numpy array/matrix)
	ADJACENCY_MATRIX  = None   # A (2D numpy array/matrix)
	TRAFFIC_MATRIX    = None   # T (dict)

	#FIXME do I need (object) or super() here?
	def __init__(self):
		self.num_channels      = 4     # 
		self.channel_init_free = False # 
		self.channel_init_bias = 0.50  # probs for a given λ be *NOT* free 
		self.multi_source_dest = True  # allow multiple source-dest. conn. pairs?

		self.wave_mtx     = None  # N copy
		self.adj_mtx      = None  # A copy
		self.traffic_mtx  = None  # T copy

		self.block_count = 0  # to store the number of blocked calls
		self.block_list  = [] # store percentage of blocked calls per generation
		self.connections = [] # store all the running lightpaths

	def get_edges(self):
		""" This method will be overriden """
		pass

	def get_nodes_2D_pos(self):
		""" This method will be overriden """
		pass

	def init_network(self):
		""" Generate matrices N, A and T """
		# define links or edges as node index pairs 
		links = self.get_edges()

		# adjacency 2D matrix: range of the values is [0,1] (int2)
		# mtx[V¹][V²] = 1 if link (V¹,V²) exists
		# mtx[V¹][V²] = 0 if link (V¹,V²) does NOT exist
		dimension = (self.num_nodes, self.num_nodes)
		adj_mtx = np.zeros(dimension, dtype=np.uint8)
		for l in links:
			adj_mtx[l[0]][l[1]] = 1
			adj_mtx[l[1]][l[0]] = adj_mtx[l[0]][l[1]] # symmetric

		# traffic matrix (dict). keys: string 'time' and lots of (ODλ)-tuple
		#  - time 3D matrix: range of the values is [0,-log(1-r)] (float)
		#     * mtx[V¹][V²][λ] = 0 if λ is free at the link (V¹,V²)
		#     * mtx[V¹][V²][λ] > 0 if λ is being used at the link (V¹,V²)
		#  - ODλ tuple: origin, destination and wavelength compose the key
		#     * value: a 2-tuple: path (tuple), holding time (np.float64)
		# right now we'll fill the traffic matrix with some random lightpaths in
		# order to start the system as if something is already running on the
		# network
		dimension = (self.num_nodes, self.num_nodes, self.num_channels)
		time_mtx = np.zeros(dimension, dtype=np.float64)
		traffic_mtx = {'time' : time_mtx}

		ch = 0
		channels = int(self.num_links*self.num_channels*self.channel_init_bias)
		while ch < channels:
			w = random.randrange(self.num_channels) # random λ 
			o = random.randrange(self.num_nodes)    # random origin node
			d = random.randrange(self.num_nodes)    # random destination node

			# avoid:
			#  - origin node equal to destination node
			#  - one-hop paths (in other words, a link)
			#  - duplicate lightpaths (same route, same wavelength)
			if o == d \
					or (o,d) in links or (d,o) in links \
					or (o,d,w) in traffic_mtx or (d,o,w) in traffic_mtx:
				continue

			# the 'if's inside the infinite loop are complementary and must:
			#  - ensure one of the routers on the new link selected is equal 
			#    to the current router, in order to form a valid path
			#  - ensure both new routers are not yet in the path, since that 
			#    would represent a loop
			#  - ensure the λ within any specific fiber link has not been taken 
			#    already, which would violate the distinct wavelength constraint
			path = []    # a single, random path to be filled
			rcurr = o    # current router (origin, for now)
			count = 0    # a counter, to avoid a real infinite loop
			while True:
				i, j = random.choice(links) 
				if i == rcurr \
						and i not in path \
						and traffic_mtx['time'][i][j][w] == 0.0:
					path.append(i)
					if j == d: # if it reaches the destination
						path.append(j)
						break # exit infinite loop
					rcurr = j # the current router is now the next one
				# remember: links are bidirectional
				if j == rcurr \
						and j not in path \
						and traffic_mtx['time'][j][i][w] == 0.0:
					path.append(j)
					if i == d: # if it reaches the destination
						path.append(i)
						break # exit infinite loop
					rcurr = i # the current router is now the next one
				count += 1
				if count > 100:
					break

			# timeout. try it again from the beginning
			if count > 100:
				continue

			# now we assign a random holding time for the wavelength λ 
			# become free again, where holding time = -ln(1-r) 
			# r must be in between (0,1), since ln(0) = +Inf and -ln(1) = 0
			r = np.random.uniform() # half-open interval [0.0, 1.0)
			while r <= 0.00000000001 or r == 1.0: # I better be sure, right?
				r = np.random.uniform()

			holding_time = -np.log(1-r)

			traffic_mtx[key] = (tuple(path), holding_time)
			for i in xrange(len(path)-1):
				rcurr = path[i]
				rnext = path[i+1]
				traffic_mtx['time'][rcurr][rnext][w] = holding_time
				traffic_mtx['time'][rnext][rcurr][w] = holding_time # symmetric

			ch += len(path)

		# wavelength availability 3D matrix: range of the values is [0,1] (int2)
		#   mtx[V¹][V²][λ] = 1 iff λ is available at the link (V¹,V²)
		#   mtx[V¹][V²][λ] = 0 iff λ is *NOT* available at the link (V¹,V²)
		#                   or if E=(V¹,V²) doesn't exist on the physical topol.
		# first, we'll make everyone available (first for loop)
		# then, we'll filter according to out traffic matrix and mark some
		# wavelengths as *NOT* free (second for(each) loop)
		# <TODO> copy adj_mtx w times </TODO>
		dimension = (self.num_nodes, self.num_nodes, self.num_channels)
		wave_mtx = np.zeros(dimension, dtype=np.uint8)
		for l in links:
			for w in xrange(self.num_channels):
				wave_mtx[l[0]][l[1]][w] = 1
				wave_mtx[l[1]][l[0]][w] = 1 # symmetric
		for conn in traffic_mtx:
			if isinstance(conn, tuple): # ensure we don't mess with the 3D mtx
				path = traffic_mtx[conn][0]
				length = len(path)
				for i in xrange(length-1):
					rcurr = path[i]
					rnext = path[i+1]
					wave_mtx[rcurr][rnext][w] = 0
					wave_mtx[rnext][rcurr][w] = 0 # symmetric

		# finally, init constants
		self.WAVELENGTH_MATRIX = wave_mtx
		self.ADJACENCY_MATRIX  = adj_mtx
		self.TRAFFIC_MATRIX    = traffic_mtx

	# update all channels that are still being used
	# TODO: just implement a foreach loop for each element on the traffic matrix
	def update_network(self, until_next):
		links_freed = {idx:[] for idx in xrange(self.num_channels)}
		for link in self.get_edges():
			i, j = link
			for w in xrange(self.num_channels):
				if self.time_mtx[i][j][w] > until_next:
					self.time_mtx[i][j][w] -= until_next # decrement time
					self.time_mtx[j][i][w]  = self.time_mtx[i][j][w] # symmetric
				else:
					self.time_mtx[i][j][w] = 0.0
					self.time_mtx[j][i][w] = self.time_mtx[i][j][w] # symmetric
					if not self.wave_mtx[i][j][w]:
						self.wave_mtx[i][j][w] = 1 # free channel (available again)
						self.wave_mtx[j][i][w] = self.wave_mtx[i][j] # symmetric
						links_freed[w].append((i,j))
						links_freed[w].append((j,i))
						#aux_yen_ff[w].append((i,j)) # FIXME

	def plot_topology(self, bestroute=False, PT_BR=False):
		""" A function to plot """
		if PT_BR:
			import sys
			reload(sys)  
			sys.setdefaultencoding('utf8') # for plot in PT_BR

		import matplotlib.pyplot as plt
		import matplotlib.animation as anim
		from matplotlib.ticker import EngFormatter

		fig = plt.figure()
		ax = fig.add_subplot(111)

		# define vertices or nodes as points in 2D cartesian plan
		nodes = self.get_nodes_2D_pos()

		# define links or edges as node index ordered pairs in cartesian plan
		links = self.get_edges()

		# show major grid lines
		ax.grid()

		# draw edges before vertices
		for link in links:
			x = [ nodes[link[0]][0], nodes[link[1]][0] ]
			y = [ nodes[link[0]][1], nodes[link[1]][1] ]
			plt.plot(x, y, 'k', linewidth=2)

		# highlight in red the shortest path with wavelength(s) available
		# a.k.a. 'best route'
		if isinstance(bestroute, list):
			for i in xrange(len(bestroute)-1):
				x = [ nodes[bestroute[i]][0], nodes[bestroute[i+1]][0] ]
				y = [ nodes[bestroute[i]][1], nodes[bestroute[i+1]][1] ]
				plt.plot(x, y, 'r', linewidth=2.5)

		# draw vertices
		i = 0
		for node in nodes:
			# parameter to adjust text on the center of the vertice
			if i < 10:
				corr = 0.060
			else:
				corr = 0.085

			plt.plot(node[0], node[1], 'wo', markersize=25)

			# write node index on the center of the node
			ax.annotate(str(i), xy=(node[0]-corr, node[1]-corr))
			i += 1
		
		# adjust values over both x and y axis 
		plt.xticks(np.arange(0, 9, 1))
		plt.yticks(np.arange(0, 7, 1))

		# finally, show the plotted graph
		plt.show(block=True)

### EOF ###

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


class Network:
	""" Network: A superclass that does something """
	def __init__(self):
		self.num_channels = 4            # 
		self.channel_free = False        # 
		self.channel_bias = [0.50, 0.50] # probs for a ch. λ be free and not, respect.
		self.multi_SD     = True         # allow multiple source-dest. conn. pairs?

	def get_edges(self):
		""" This method will be overriden """
		pass

	def get_nodes_2D_pos(self):
		""" This method will be overriden """
		pass

	def generate_network(self):
		""" Generate matrices N, A and T """
		# define links or edges as node index pairs 
		links = self.get_edges()

		# wavelength availability 3D matrix: range of the values is [0,1] (int2)
		# mtx[V¹][V²][λ] = 1 if the wavelength λ is available at the link (V¹,V²)
		# mtx[V¹][V²][λ] = 0 if the wavelength λ is NOT available at the link (V¹,V²)
		#                 or if E=(V¹,V²) doesn't exist on the physical topology
		dimension = (self.num_nodes, self.num_nodes, self.num_channels)
		wave_mtx = np.zeros(dimension, dtype=np.uint8)
		for l in links:
			for w in xrange(self.num_channels):
				availability = np.random.choice((0,1), p=self.channel_bias)
				wave_mtx[l[0]][l[1]][w] = availability
				wave_mtx[l[1]][l[0]][w] = wave_mtx[l[0]][l[1]][w] # symmetric

		# adjacency 2D matrix: range of the values is [0,1] (int2)
		# mtx[V¹][V²] = 1 if link (V¹,V²) exists
		# mtx[V¹][V²] = 0 if link (V¹,V²) does NOT exist
		dimension = (self.num_nodes, self.num_nodes)
		adj_mtx = np.zeros(dimension, dtype=np.uint8)
		for l in links:
			adj_mtx[l[0]][l[1]] = 1
			adj_mtx[l[1]][l[0]] = adj_mtx[l[0]][l[1]] # symmetric

		# traffic time 3D matrix: range of the values is [0,1] (float)
		# mtx[V¹][V²][λ] = 0 if the wavelength λ is free at the link (V¹,V²)
		# mtx[V¹][V²][λ] > 0 if the wavelength λ is being used at the link (V¹,V²)
		dimension = (self.num_nodes, self.num_nodes, self.num_channels)
		time_mtx = np.zeros(dimension, dtype=np.float64)
		for l in links:
			for w in xrange(self.num_channels):
				# check if λ is *NOT* available
				# then assign a random holding time for it to become free again
				# where holding time = -ln(1-r) 
				# r must be in between (0,1), since ln(0) = +Inf and -ln(1) = 0
				if not wave_mtx[l[0]][l[1]][w]:
					r = np.random.uniform() # half-open interval [0.0, 1.0)
					while r == 0.0 or r == 1.0: # I better be sure, right?
						r = np.random.uniform()
					time_mtx[l[0]][l[1]][w] = -np.log(1-r)
					time_mtx[l[1]][l[0]][w] = time_mtx[l[0]][l[1]][w] # symmetr.

		return wave_mtx, adj_mtx, time_mtx


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

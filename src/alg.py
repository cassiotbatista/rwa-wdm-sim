#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm
# Routing and Wavelength Assignment
# General Objective Function
#
# Author: Apr 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last edited on March 2018
#
# References:
# - random 'biased' choice: https://stackoverflow.com/q/25507558
# - import from parent dir: https://stackoverflow.com/a/30536516
# - multiple inheritance:   https://stackoverflow.com/q/3277367

class Routing(object):
	#FIXME do I need (object) or super() here?
	def __init__(self):
		pass

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.shortest_paths.html
	# FIXME
	def dijkstra(self, adj_mtx, s, d):
		""" Certainly does something """
		if any([s,d])<0 or any([s,d])>adj_mtx.shape[0] or s == d:
			print 'Error: source (%d) or destination (%d) indexes are invalid' % (s,d)
			return None
		G = nx.from_numpy_matrix(adj_mtx, create_using=nx.Graph())
		hops, path = nx.bidirectional_dijkstra(G, s, d, weight=None)
		return path

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.simple_paths.html
	# FIXME
	def yen(self, mat, (s,d), k):
		if any([s,d])<0 or any([s,d])>mat.shape[0] or k<0:
			print 'Error'
			return None
		G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
		paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
		return paths[:k]

class WavelengthAssignment(object):
	#FIXME do I need (object) or super() here?
	def __init__(self):
		pass

	# local knowledge first fit wavelength assignment
	# FIXME
	def first_fit(self, N, R, num_channels):
		""" Certainly does something """
		rcurr, rnext = R[0], R[1] # look at the source node only (1st link)
		# Check whether each wavelength w is available 
		# on the first link of route R (only at the 1st link)
		for w in xrange(num_channels):
			if N[rcurr][rnext][w]:
				# automatically checks if the wavelength is available 
				# * ONLY at the output of the node *
				return self.check_local_availability(N, R, w)

		return None # block

	# https://networkx.github.io/documentation/development/...
	# ... reference/algorithms.coloring.html
	# FIXME
	def greedy_color(self, H, colors, strategy=nx.coloring.strategy_largest_first):
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
	
			# assign the node the newly found color
			#colors[node] = color
			return color

		#return colors


class RWAAlgorithm(Routing, WavelengthAssignment):
	""" This class certainly does something """
	def __init__(self):
		super(RWAAlgorithm).__init__(self)
		self.block_count = 0  # to store the number of blocked calls
		self.block_list  = [] # store percentage of blocked calls per generation

	def routing(self):
		""" This method will be overriden """
		pass

	def wavelength_assignment(self):
		""" This method will be overriden """
		pass

	# FIXME
	def check_global_availability(self):
		# GLOBAL KNOWLEDGE first fit wavelength assignment
		color = None
		for R in routes:
			avail = 2**info.NSF_NUM_CHANNELS-1
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				avail &= N[rcurr][rnext]

				if avail == 0:
					break

			if avail > 0:
				color = format(avail, '0%db' % info.NSF_NUM_CHANNELS)[::-1].index('1')
				break

	# FIXME
	def check_local_availability(self, wave_mtx, route, wavelength):
		""" local knowledge wavelength assignment """
		# check if the λ chosen at the first link is availble on all links of R
		length = len(route)
		for r in xrange(length-1):
			rcurr = route[r]
			rnext = route[r+1]

			# if not available in any of the next links, block
			if not N[rcurr][rnext][wavelength]:
				return None # blocked

		return wavelength

	def plot_fits(self, fits, PT_BR=False):
		""" This method plots """
		if PT_BR:
			import sys
			reload(sys)  
			sys.setdefaultencoding('utf8') # for plot in PT_BR

		import matplotlib.pyplot as plt
		import matplotlib.animation as anim
		from matplotlib.ticker import EngFormatter

		# do not interrupt program flow to plot
		plt.interactive(True) 

		fig, ax = plt.subplots()
		ax.set_xscale('linear')

		formatter = EngFormatter(unit='', places=1)
		ax.xaxis.set_major_formatter(formatter)

		if PT_BR:
			ax.set_xlabel(u'Gerações', fontsize=20)
			ax.set_ylabel(u'Número de chamadas atendidas', fontsize=20)
		else:
			ax.set_xlabel(u'Generations', fontsize=20)
			ax.set_ylabel(u'Number of attended calls', fontsize=20)
	
		ax.grid()
		ax.plot(fits, linewidth=2.0)
	
		x = range(0, 0, 5) # FIXME
		y = np.arange(0, 8, 1)
	
		if PT_BR:
			title =  u'Melhores fits de %d indivíduos por geração' % 0
		else:
			title =  u'Best fit values of %d individuals per generation' % 0

		fig.suptitle(title, fontsize=20)

		#plt.margins(0.02)
		plt.subplots_adjust(bottom=0.12)
	
		#plt.xticks(x)
		plt.yticks(y)
		plt.draw()
		plt.show(block=True)

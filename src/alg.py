#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA Simulator
# Routing and Wavelength Assignment with Static Traffic Simulator for
# All-Optical WDM Networks
#
# Author: Apr 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last edited on March 2018
#
# References:
# - import from parent dir: https://stackoverflow.com/a/30536516
# - multiple inheritance:   https://stackoverflow.com/q/3277367

import sys
import os

import numpy as np
import info
import networkx as nx
import itertools

#FIXME
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class Routing(object):
	""" Class Routing """

	def __init__(self):
		pass

	def is_od_pair_ok(self, adj_mtx, orig, dest):
		if orig == dest:
			return False
		# TODO those two 'elif's below are really really necessary?
		elif orig < 0 or dest < 0: 
			sys.stderr.write('ta caindo o forninho\n')
			sys.stderr.flush()
			return False
		elif orig > adj_mtx.shape[0] or dest > adj_mtx.shape[0]:
			sys.stderr.write('ta caindo o forninho\n')
			sys.stderr.flush()
			return False
		else:
			return True

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.shortest_paths.html
	def dijkstra(self, A, o, d):
		""" Certainly does something """

		if not self.is_od_pair_ok(A, o, d):
			sys.stderr.write('Error: source (%d) or destination (%d) ' % (o,d))
			sys.stderr.write('indexes are invalid.\n')
			sys.stderr.flush()
			return None

		G = nx.from_numpy_matrix(A, create_using=nx.Graph())
		hops, path = nx.bidirectional_dijkstra(G, o, d, weight=None)
		return path

	# https://networkx.github.io/documentation/networkx-1.10/...
	# ... reference/algorithms.simple_paths.html
	def yen(self, A, o, d, k):
		""" Apply k-shortest path algorithm for routing only """

		if not self.is_od_pair_ok(A, o, d) or k < 0:
			sys.stderr.write('Error: source (%d) or destination (%d) ' % (s,d))
			sys.stderr.write('indexes might be invalid.\n')
			sys.stderr.write('Check the k value (%d) as well.\n' % k)
			sys.stderr.flush()
			return None

		G = nx.from_numpy_matrix(A, create_using=nx.Graph())
		paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
		return paths[:k]

class WavelengthAssignment(object):
	""" Class Wavelength Assignment """

	def __init__(self):
		pass

	# local knowledge first fit wavelength assignment
	def first_fit(self, W, route, num_channels):
		""" Certainly does something """

		# look at the source node only (1st link)
		rcurr = route[0] 
		rnext = route[1]
		# Check whether each wavelength w is available 
		# on the first link of route R (only at the 1st link)
		for w in xrange(num_channels):
			# if the wavelength is available at the output node
			if W[rcurr][rnext][w]:
				# return it as the first one who fits :)
				return w

		return None # no wavelength available at the output of the source node

	def share_edge(self, p):
		""" a method to check if two physical paths have a physical link in common """

		# gambiarra: 'listerator' to avoid using two variables
		r = [None, None] 
		for r[0] in xrange(1, len(p[0])):
			for r[1] in xrange(1, len(p[1])):
				# check directly equal links
				# 0 5 6 7 8 [9 12]
				# 0 1 3 4   [9 12]
				if p[0][r[0]-1] == p[1][r[1]-1] and p[0][r[0]] == p[1][r[1]]:
					return True
				# check reversely equal links: graph is bidirectional
				# 0     [5 6]  7  8 9 12
				# 0 1 3 [6 5] 10 12
				elif p[0][r[0]] == p[1][r[1]-1] and p[0][r[0]-1] == p[1][r[1]]:
					return True
		return False

	def g2h(self, G, route, key):
		""" pre-step for greedy coloring: convert a graph G to a graph H """

		# gambiarra: the new connection must be at the traffic matrix before
		# starting coloring the vertices
		traffic_mtx[key] = {tuple(route):0.00}
		num_calls = G['num_calls']+1 # consider the path you're goin to assign a λ

		H = np.zeros((num_calls,num_calls), dtype=np.uint8)

		i = 0
		j = 0
		colors = {}
		# OBS.: @key_x = tuple(ODλ), @path_x = tuple(0,2,5,12)
		for key_i in G:
			if not isinstance(key_i, tuple):
				continue
			if G[key_i][2] != -1:
				colors[i] = G[key_i][2] # FIXME get wavelength
			for key_j in G:
				if not isinstance(key_j, tuple):
					continue
				# check if tuples are direcly or reversely equal (OD <-> OD|DO)
				elif is_same_traffic_entry(key_i, key_j):
					continue
				# cross compare paths i & j
				for path_i in G[key_i]:
					i += 1 # keep track of the counter
					for path_j in G[key_j]:
						j += 1 # keep track of the counter
						# cross compare each and every router of i & j
						if self.share_edge((path_i, path_j)):
							H[i][j] = 1
							H[i][j] = 1

		return H, colors

	# https://networkx.github.io/documentation/development/...
	# ... reference/algorithms.coloring.html
	# FIXME
	def greedy_color(self, H, colors, strategy=nx.coloring.strategy_largest_first):
		""" vertex coloring """

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

	def random(self):
		pass

	def most_used(self):
		pass

	def least_used(self):
		pass

class RWAAlgorithm(Routing, WavelengthAssignment):
	""" This class certainly does something """

	def __init__(self):
		super(RWAAlgorithm, self).__init__()
		self.block_count = {} # to store the number of blocked calls
		self.block_dict  = {} # store percentage of blocked calls per generation

	def is_wave_available(self, wave_mtx, route, wavelength):
		""" check if a wavelength is available over all links of the path """

		# check if the λ chosen at the first link is availble on all links of R
		length = len(route)
		for r in xrange(length-1):
			rcurr = route[r]
			rnext = route[r+1]

			# if not available in any of the next links, block
			if not wave_mtx[rcurr][rnext][wavelength]:
				return False # call must be blocked

		return True

	def alloc_net_resources(self, net, route, o, d, w, ht):
		""" eita giovana """

		# update traffic matrix 1/2: tuple dicts
		key = (o, d, w)
		net.traffic_mtx[key].update({tuple(route):ht})

		# increase traffic matrix's call counter
		net.traffic_mtx['num_calls'] += 1 

		# update trafffic matrix 2/2: np 3D array
		length = len(route)
		for r in xrange(length-1):
			rcurr = route[r]
			rnext = route[r+1]

			# make λ NOT available on all links of the path 
			# do not forget to make the wavelength matrix symmetrical
			net.wave_mtx[rcurr][rnext][w] = 0
			net.wave_mtx[rnext][rcurr][w] = 0 # symmetric
	
			# assign a time for it to be free again (released)
			# do not forget to make the traffic matrix symmetrical
			net.traffic_mtx['time'][rcurr][rnext][w] = ht
			net.traffic_mtx['time'][rnext][rcurr][w] = ht # symmetric

	# https://docs.scipy.org/doc/numpy-1.13.0/reference/generated/numpy.append.html
	def save_erlang_blocks(self, net_key, net_num_nodes, total_calls):
		for node in xrange(net_num_nodes):
			# compute a percentage of blocking probability per Erlang
			bp_per_erlang = 100.0 * self.block_count[net_key][node] / total_calls 
			self.block_dict[net_key][node] = np.append(
					self.block_dict[net_key][node], bp_per_erlang)

	# https://docs.scipy.org/doc/numpy-1.14.0/reference/generated/numpy.savetxt.html
	# numpy append to file with savetxt() - https://stackoverflow.com/q/27786868
	def save_blocks_to_file(self, basedir, net_name, net_num_nodes, ch_n):
		""" This does something """

		# e.g.: DFF_ARPA_8ch.txt
		blockfilename = '%s_%s_%dch.txt' % (self.name, net_name, ch_n)
		with open(blockfilename, 'a') as blockfile:
			for node in xrange(net_num_nodes):
				np.savetxt(os.path.join(basedir, blockfile),
						self.block_dict[net_name][node], fmt='%6.2f', comments='',
						delimiter=',', header='<block>', footer='</block>\n')

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

	# TODO
	def plot_bp(self, net):
		""" Plot blocing probabilities """

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

class DijkstraFirstFit(RWAAlgorithm):
	""" Dijkstra and First Fit """

	def __init__(self):
		super(DijkstraFirstFit, self).__init__()
		self.name     = 'DFF'
		self.fullname = 'Dijkstra and First Fit'

	def rwa(self, net, orig, dest, hold_t)
		""" This method RWAs """
		# call the routing method
		route = self.dijkstra(net.adj_mtx, orig, dest)

		# call the wavelength assignment method
		wavelength = self.first_fit(net.wave_mtx, route, net.num_channels)

		# if WA was successful, allocate resources on the network
		if wavelength is not None:
			# but first things first: we need to check whether this same
			# *FIRST λ* is available on all links of the path in order to
			# establish a connection over it
			if self.is_wave_available(net.wave_mtx, route, wavelength):
				# now we can establish a connection. so let's allocate
				# resources of the network for this call
				self.alloc_net_resources(net,
						route, orig, dest, wavelength, hold_t)
			return 0 # allocated

		return 1 # block

# FIXME FIXME FIXME
class DijkstraGraphColoring(RWAAlgorithm):
	""" Dijkstra + Graph Coloring """

	def __init__(self):
		super(DijkstraGraphColoring, self).__init__()

	def rwa(net, orig, dest, hold_t)
		# call the routing method
		route = self.dijkstra(net.adj_mtx, orig, dest)

		# convert a graph of connections (G, traffic mtx) to an aux graph H
		invalid_key = (orig, dest, -1)
		H, colors = self.g2h(net.traffic_mtx, route, invalid_key)

		# call the wavelength assignment method over the route
		# NOTE: g2h() already puts the current route on the traffic matrix
		# under an invalid key
		wavelength = self.greedy_color(H, colors)

		# if WA was successful, let's allocate resources on the network
		if color < net.num_channels:
			# but first things first: we need to check whether this same *λ* is
			# available on all links of the path in order to establish a
			# connection over it
			if self.is_wave_available(net.wave_mtx, route, wavelength):
				# now we can establish a connection. so let's pop the last
				# connection appended to traffic matrix and allocate resources
				# of the network for this call, also assigning the call for a
				# proper key ODλ
				net.traffic_mtx.pop(invalid_key)
				self.alloc_net_resources(net,
						route, orig, dest, wavelength, hold_t)
				return 0 # allocated

		# pop the invalid connection from traffic mtx before finally blocking
		# the call
		net.traffic_mtx.pop(invalid_key)
		return 1 # blocked

# FIXME FIXME FIXME
class YenGraphColoring(RWAAlgorithm):
	""" Yen + Greedy Coloring """

	def __init__(self, k):
		super(YenGraphColoring, self).__init__()
		self.k = k 

	def rwa(self, net, orig, dest, hold_t):
		# call the routing method. Here, the method returns multiple routes
		routes = self.yen(net.adj_mtx, orig, dest, self.k)

		for route in routes:
			# convert a graph of connections (G, traffic mtx) to an aux graph H
			invalid_key = (orig, dest, -1)
			H, colors = self.g2h(net.traffic_mtx, route, invalid_key)

			# call the wavelength assignment method over the current route
			# NOTE: g2h() already puts the current route on the traffic matrix
			# under an invalid key
			wavelength = self.greedy_color(H, colors)

			# if WA was successful, let's allocate resources on the network
			if color < net.num_channels:
				# but first things first: we need to check whether this same
				# *λ* is available on all links of the path in order to
				# establish a connection over it
				if self.is_wave_available(net.wave_mtx, route, wavelength):
					# now we can establish a connection. so let's pop last
					# connection appended to traffic matrix and allocate
					# resources of the network for this call, also assigning
					# the call for a proper key ODλ
					net.traffic_mtx.pop(invalid_key)
					self.alloc_net_resources(net,
							route, orig, dest, wavelength, hold_t)
					return 0 # allocated

			# try another route insted of blocking immediately
			# pop the invalid connection from traffic mtx before trying again
			net.traffic_mtx.pop(invalid_key)

		return 1 # blocked

class YenFirstFit(RWAAlgorithm):
	""" A class that does something """

	def __init__(self, k):
		super(YenFirstFit, self).__init__()
		self.k = k

	def rwa(self, net, orig, dest, hold_t):
		# call the routing method. Here, the method returns multiple routes
		routes = self.yen(net.adj_mtx, orig, dest, self.k)

		for route in routes:
			# call the wavelength assignment method over the current route
			wavelength = self.first_fit(net.wave_mtx, route, net.num_channels)

			# if WA was successful, let's allocate resources on the network
			if wavelength is not None:
				# but first things first: we need to check whether this same
				# *FIRST λ* is available on all links of the path in order to
				# establish a connection over it
				if self.is_wave_available(net.wave_mtx, route, wavelength):
					# now we can establish a connection. so let's allocate
					# resources of the network for this call
					self.alloc_net_resources(net,
							route, orig, dest, wavelength, hold_t)
					return 0 # allocated

			# TIP: if WA wasn't successfull, we give chance to another route,
			# because this current one does not have a wavelength available over
			# all its links

		return 1 # blocked

# TODO: Main Genetic Algorithm Function
class GeneticAlgorithm(RWAAlgorithm, Environment)
	""" GA class """

	def __init__(self, GA_SIZE_POP,
					GA_MIN_GEN, GA_MAX_GEN,
					GA_MIN_CROSS_RATE, GA_MAX_CROSS_RATE,
					GA_MIN_MUT_RATE, GA_MAX_MUT_RATE,
					GA_GEN_INTERVAL):
		super(GeneticAlgorithm, self).__init__()
		self.GA_SIZE_POP       = GA_SIZE_POP
		self.GA_MIN_GEN        = GA_MIN_GEN
		self.GA_MAX_GEN        = GA_MAX_GEN
		self.GA_MIN_CROSS_RATE = GA_MIN_CROSS_RATE
		self.GA_MAX_CROSS_RATE = GA_MAX_CROSS_RATE
		self.GA_MIN_MUT_RATE   = GA_MIN_MUT_RATE
		self.GA_MAX_MUT_RATE   = GA_MAX_MUT_RATE
		self.GA_GEN_INTERVAL   = GA_GEN_INTERVAL

	def rwa(self, net, orig, dest, hold_t):
		population = self.init_population(net.adj_mtx, net.num_nodes, orig, dest)
		fits = []
		while not stop_criteria:
			# perform evaluation (fitness calculation)
			for ind in xrange(len(population)):
				L, wl_avail, r_len = self.evaluate(net, population[ind][0])
				population[ind][1] = L
				population[ind][2] = wl_avail
				population[ind][3] = r_len

			# perform selection
			mating_pool = self.select(list(population), self.GA_MAX_CROSS_RATE)

			# perform crossover
			offspring = self.cross(mating_pool)
			if offspring:
				for child in offspring:
					population.pop()
					population.insert(0, [child, [], 0, 0])

			# perform mutation
			for i in xrange(int(math.ceil(self.GA_MIN_MUT_RATE*len(population)))):
				normal_ind = random.choice(population)
				trans_ind = self.mutate(net.adj_mtx, normal_ind[0]) # X MEN
				if trans_ind != normal_ind:
					population.remove(normal_ind)
					population.insert(0, [trans_ind, [], 0, 0])

			# sort population according to length .:. shortest paths first
			population.sort(key=itemgetter(2), reverse=True)

			# sort population according to wavelength availability
			population = self.insertion_sort(population)

		# perform evaluation (fitness calculation)
		for ind in xrange(len(population)):
			L, wl_avail, r_len = evaluate(population[ind][0], N)
			population[ind][1]  = L
			population[ind][2]  = wl_avail
			population[ind][3]  = r_len

		# sort population according to length: shortest paths first
		population.sort(key=itemgetter(2), reverse=True)

		# sort population according to wavelength availability
		population = self.insertion_sort(population)
		
		# update NSF graph
		route = population[0][0]
		if population[0][2] > 0:
			wavelength = population[0][1].index(1)
			self.alloc_net_resources(net, route, orig, dest, wavelength, hold_t)
			return 0 # allocated

		return 1 # blocked

### EOF ###

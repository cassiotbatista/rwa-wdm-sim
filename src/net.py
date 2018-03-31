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
# Last edited on Mar 2018

import random
import numpy as np

class Network(object):
	""" Network: A superclass that does something """
	# T's inspiration: http://fnss.github.io/doc/core/apidoc/fnss.classes.html
	__wavelength_matrix = None   # W (3D numpy array/matrix)
	__adjacency_matrix  = None   # A (2D numpy array/matrix)
	__traffic_matrix    = None   # T (dict)

	def __init__(self, ch_n, ch_free, ch_bias):
		self.num_channels      = ch_n    # int
		self.channel_init_free = ch_free # bool
		self.channel_init_bias = ch_bias # probs for a given λ be *NOT* free 
		self.allow_multi_od    = True    # allow multiple OD conn. pairs?

		self.wave_mtx     = None  # W copy
		self.adj_mtx      = None  # A copy
		self.traffic_mtx  = None  # T copy

	def get_edges(self):
		""" This method will be overriden """
		pass

	def get_nodes_2D_pos(self):
		""" This method will be overriden """
		pass

	def init_network(self):
		""" Generate matrices W, A and T """
		# define links or edges as node index pairs 
		links = self.get_edges()

		# adjacency 2D matrix: range of the values is [0,1] (int2)
		# mtx[V¹][V²] = 1 if link (V¹,V²) exists
		# mtx[V¹][V²] = 0 if link (V¹,V²) does NOT exist
		dimension = (self.num_nodes, self.num_nodes)
		a_mtx = np.zeros(dimension, dtype=np.uint8)
		for l in links:
			a_mtx[l[0]][l[1]] = 1
			a_mtx[l[1]][l[0]] = a_mtx[l[0]][l[1]] # symmetric

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
		t_mtx = {'time':time_mtx, 'num_conn':0} # init the number of running connections

		# the percentage of occupied channels is defined by the bias parameter
		#   nlinks * nchannels ---> 100 %             # λ total
		#        ch_occup      ---> chbias * 100 %    # λ not free
		ch_i = 0 # channel counter/iterator over the nº of λ occupied below
		n_ch_occup = int(self.num_links*self.num_channels*self.channel_init_bias)
		while ch_i < n_ch_occup:
			w = random.randrange(self.num_channels) # random λ 
			o = random.randrange(self.num_nodes)    # random origin node
			d = random.randrange(self.num_nodes)    # random destination node

			# avoid:
			#  - origin node equal to destination node
			#  - one-hop paths (in other words, a link)
			if o == d or (o,d) in links or (d,o) in links:
				continue

			# the 'if' inside the inf loop must ensure:
			#  - one of the routers on the new link selected is equal to the
			#    current router, in order to form a valid path
			#  - both new routers are not yet in the path, since that would
			#    represent a loop
			#  - the λ within any specific fiber link has not been taken
			#    already, which would violate the distinct wavelength constraint
			route = []   # a single, random path to be filled
			rcurr = o    # current router (origin, for now)
			trials = 0    # a counter, to avoid a real infinite loop
			while True:
				x, y = random.choice(links) 
				for i, j in [(x,y), (y,x)]: # remember: links are bidirectional
					if i == rcurr \
							and i not in route and j not in route \
							and t_mtx['time'][i][j][w] == 0.0:
						route.append(i)
						trials -= 2
						if j == d: # if it reaches the destination
							route.append(j)
							break # exit infinite loop
						rcurr = j # else: the current router is now the next one

				trials += 1
				if trials > 150: # timeout. try it again from the beginning
					route  = []
					rcurr  = o
					trials = 0
					continue

			# avoid duplicate lightpaths (same route, same wavelength)
			route = tuple(route)
			for key in [(o,d,w), (d,o,w)]:
				if key in t_mtx:
					for lightpath in t_mtx[key]:
						if lightpath == route:
							continue 
					break # keep the 'key' variable

			# now we assign a random holding time for the wavelength λ 
			# become free again, where holding time = -ln(1-r) 
			# r must be in between (0,1), since ln(0) = +Inf and -ln(1) = 0
			r = np.random.uniform() # half-open interval [0.0, 1.0)
			while r <= 0.00000000001 or r == 1.0: # I better be sure, right?
				r = np.random.uniform()

			holding_time = -np.log(1-r)

			# add connection to traffic matrix
			# to ease localization, also update a time matrix embedded within
			# the traffic matrix (dict) data structure
			t_mtx[key].update({route:holding_time})
			for i in xrange(len(route)-1):
				rcurr = route[i]
				rnext = route[i+1]
				t_mtx['time'][rcurr][rnext][w] = holding_time
				t_mtx['time'][rnext][rcurr][w] = holding_time # symmetric
				ch_i += 1 # update channel counter

			t_mtx['num_conn'] += 1 # update the number of running connections
			route = [] # flush path to calculate a new, fresh one

		# wavelength availability 3D matrix: range of the values is [0,1] (int2)
		#   mtx[V¹][V²][λ] = 1 iff λ is available at the link (V¹,V²)
		#   mtx[V¹][V²][λ] = 0 iff λ is *NOT* available at the link (V¹,V²)
		#                   or if E=(V¹,V²) doesn't exist on the physical topol.
		# first, we'll make everyone available (first nested loop in @l)
		# then, we'll filter according to the connections on our traffic matrix 
		# and mark some wavelengths as *NOT* free (second nested loop in @conn)
		dimension = (self.num_nodes, self.num_nodes, self.num_channels)
		w_mtx = np.zeros(dimension, dtype=np.uint8)
		for i, j in links:
			for w in xrange(self.num_channels):
				w_mtx[i][j][w] = 1
				w_mtx[j][i][w] = 1 # symmetric
		for conn in t_mtx:
			# ensure we don't mess with the 3D mtx, getting then a (ODλ) tuple
			# if a connection exists, mark the wavelength as 'occupied'
			if isinstance(conn, tuple):
				w = conn[2]
				for path in t_mtx[conn]:
					for i in xrange(len(path)-1):
						rcurr = path[i]
						rnext = path[i+1]
						w_mtx[rcurr][rnext][w] = 0
						w_mtx[rnext][rcurr][w] = 0 # symmetric

		# finally, init constants
		self.__wavelength_matrix = w_mtx
		self.__adjacency_matrix  = a_mtx
		self.__traffic_matrix    = t_mtx

	def reset_network(self):
		self.wave_mtx    = self.__wavelength_matrix.copy() # matrix
		self.adj_mtx     = self.__adjacency_matrix.copy()  # matrix
		self.traffic_mtx = self.__traffic_matrix.copy()    # dict

	# on traffic matrix, update all channels that are still being used
	# dict size-changed RuntimeError exc. - https://stackoverflow.com/q/11941817
	def update_network(self, until_next):
		""" A method that does something """
		for key in self.traffic_mtx.keys(): 
			if not isinstance(key, tuple): # ensure we don't mess with the 3D mtx
				continue # because we want @key to be (ODλ)
			w = key[2] # extract λ in question
			for path in self.traffic_mtx[key].keys():
				if self.traffic_mtx[key][path] > until_next:
					# update both dict value and time matrix values
					self.traffic_mtx[key][path] -= until_next
					for i in xrange(len(path)-1):
						rcurr = path[i]
						rnext = path[i+1]
						self.traffic_mtx['time'][rcurr][rnext][w] -= until_next
						self.traffic_mtx['time'][rnext][rcurr][w] -= until_next
				else:
					# remove lightpath from traffic matrix (pop) and update both
					# time and wavelength availability matrices
					self.traffic_mtx[key].pop(path)
					for i in xrange(len(path)-1):
						rcurr = path[i]
						rnext = path[i+1]
						# the time until the next call is now 0, since the
						# connection that was withholding λ it is gone
						self.traffic_mtx['time'][rcurr][rnext][w] = 0.0
						self.traffic_mtx['time'][rnext][rcurr][w] = 0.0
						# do not forget to free the respective λ as well
						self.wave_mtx[rcurr][rnext][w] = 1
						self.wave_mtx[rnext][rcurr][w] = 1

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

class AdvancedResearchProjectsAgency(Network): 
	""" U.S. Advanced Research Projects Agency (ARPANET) """
	def __init__(self):
		super(AdvancedResearchProjectsAgency, super).__init__()
		self.name        = 'ARPA'
		self.fullname    = 'Advanced Research Projects Agency'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False FIXME
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,2), (0,19),  #  0
			(1,2), (1,3),          #  1
			(2,4),                 #  2
			(3,4), (3,5),          #  3
			(4,6),                 #  4
			(5,6), (5,7),          #  5
			(6,9),                 #  6
			(7,8), (7,9), (7,10),  #  7
			(8,9), (8,19),         #  8
			(9,15),                #  9
			(10,11), (10,12),      # 10
			(11,12),               # 11
			(12,13),               # 12
			(13,14), (13,16),      # 13
			(14,15),               # 14
			(15,17), (15,18),      # 15
			(16,17), (16,19),      # 16
			(17,18)                # 17
		]

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
	
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
			['0',  (1.80, 5.70)], #  0
			['1',  (2.80, 5.00)], #  1
			['2',  (3.40, 6.30)], #  2
			['3',  (3.40, 5.50)], #  3
			['4',  (4.50, 5.60)], #  4
			['5',  (4.70, 4.60)], #  5
			['6',  (5.30, 4.80)], #  6
			['7',  (3.60, 4.40)], #  7
			['8',  (2.20, 4.00)], #  8
			['9',  (4.80, 3.50)], #  9
			['10', (2.40, 2.60)], # 10
			['11', (2.50, 1.50)], # 11
			['12', (1.40, 2.30)], # 12
			['13', (1.80, 3.20)], # 13
			['14', (3.70, 2.70)], # 14
			['15', (5.20, 2.50)], # 15
			['16', (0.80, 3.90)], # 16
			['17', (1.20, 0.50)], # 17
			['18', (3.60, 0.80)], # 18
			['19', (0.80, 5.50)]  # 19
		]

class CooperacionLatinoAmericana(Network): 
	""" Cooperación Latino Americana de Redes Avanzadas (RedClara) """
	def __init__(self):
		super(CooperacionLatinoAmericana, self).__init__()
		self.name        = 'CLARA'
		self.fullname    = u'Cooperación Latino Americana de Redes Avanzadas'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False FIXME
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,5), (0,8), (0,11),  #  0
			(1,2),                        #  1
			(2,3),                        #  2
			(3,4),                        #  3
			(4,5),                        #  4
			(5,6), (5,7), (5,11),         #  5
			(7,8),                        #  7
			(8,9), (8,11),                #  8
			(9,10), (9,11),               #  9
			(11,12)                       # 11
		]

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
	
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
			['US', (2.00, 6.00)], #  0
			['MX', (1.00, 6.00)], #  1
			['GT', (1.00, 4.50)], #  2
			['SV', (1.00, 2.50)], #  3
			['CR', (1.00, 1.00)], #  4
			['PN', (2.00, 1.00)], #  5
			['VE', (1.50, 1.70)], #  6
			['CO', (3.00, 1.00)], #  7
			['CL', (4.00, 1.00)], #  8
			['AR', (5.00, 3.50)], #  9
			['UY', (5.00, 1.00)], # 10
			['BR', (4.00, 6.00)], # 11
			['UK', (5.00, 6.00)]  # 12
		]

class Italian(Network): 
	""" Italian Network (NSFNET) """
	def __init__(self):
		super(Italian, self).__init__()
		self.name        = 'ITA'
		self.fullname    = u'Italian'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,2),                        #  0
			(1,2), (1,3), (1,4),                 #  1
			(2,7), (2,8), (2,9),                 #  2
			(3,4), (3,5),                        #  3
			(4,6), (4,7),                        #  4
			(5,6),                               #  5
			(6,7),                               #  6
			(7,9), (7,10),                       #  7
			(8,9), (8,12),                       #  8
			(9,11), (9,12),                      #  9
			(10,13),                             # 10
			(11,12), (11,13),                    # 11
			(12,14), (12,20),                    # 12
			(13,14), (13,15),                    # 13
			(14,15), (14,16), (14,18), (14,19),  # 14
			(15,16),                             # 15
			(16,17),                             # 16
			(17,18),                             # 17
			(18,19),                             # 18
			(19,20)                              # 19
		]

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
	
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
			['x', (0.70, 6.50)], #  0 
			['x', (1.80, 7.00)], #  1
			['x', (1.80, 6.00)], #  2
			['x', (3.00, 7.70)], #  3
			['x', (2.70, 6.80)], #  4
			['x', (4.00, 6.70)], #  5
			['x', (3.30, 6.30)], #  6
			['x', (2.90, 5.70)], #  7
			['x', (2.00, 5.00)], #  8
			['x', (2.90, 5.00)], #  9
			['x', (3.80, 5.20)], # 10
			['x', (3.20, 4.50)], # 11
			['x', (2.50, 3.50)], # 12
			['x', (3.90, 4.00)], # 13
			['x', (3.70, 2.50)], # 14
			['x', (4.90, 3.00)], # 15
			['x', (4.50, 2.00)], # 16
			['x', (4.70, 1.00)], # 17
			['x', (3.80, 0.50)], # 18
			['x', (2.70, 0.60)], # 19
			['x', (1.20, 1.50)]  # 20
		]

class JointAcademic(Network): 
	""" U.K. Joint Academic Network (JANET) """
	def __init__(self):
		super(JointAcademic, self).__init__()
		self.name        = 'JANET'
		self.fullname    = 'Joint Academic Network'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False # FIXME
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,2),                # 0
			(1,2), (1,3),                # 1
			(2,4),                       # 2
			(3,4), (3,5), #(3,6),        # 3
			(4,6),                       # 4
			(5,6)                        # 5
		]

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
			['Gla', (1.50, 4.00)], # 0
			['Man', (1.00, 3.00)], # 1
			['Lee', (2.00, 3.00)], # 2
			['Bir', (1.00, 2.00)], # 3
			['Not', (2.00, 2.00)], # 4
			['Bri', (1.00, 1.00)], # 5
			['Lon', (2.00, 1.00)]  # 6
		]

class NationalScienceFoundation(Network): 
	""" U.S. National Science Foundation Network (NSFNET) """
	def __init__(self):
		super(NationalScienceFoundation, self).__init__()
		self.name        = 'NSF'
		self.fullname    = 'National Science Foundation'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,2), (0,5),   #  0
			(1,2), (1,3),          #  1
			(2,8),                 #  2
			(3,4), (3,6), (3,13),  #  3
			(4,9),                 #  4
			(5,6), (5,10),         #  5
			(6,7),                 #  6
			(7,8),                 #  7
			(8,9),                 #  8
			(9,11), (9,12),        #  9
			(10,11), (10,12),      # 10
			(11,13)                # 11
		]

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
	
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
			['0',  (0.70, 2.70)], #  0
			['1',  (1.20, 1.70)], #  1
			['2',  (1.00, 4.00)], #  2
			['3',  (3.10, 1.00)], #  3
			['4',  (4.90, 0.70)], #  4
			['5',  (2.00, 2.74)], #  5
			['6',  (2.90, 2.66)], #  6
			['7',  (3.70, 2.80)], #  7
			['8',  (4.60, 2.80)], #  8
			['9',  (5.80, 3.10)], #  9
			['10', (5.50, 3.90)], # 10
			['11', (6.60, 4.60)], # 11
			['12', (7.40, 3.30)], # 12
			['13', (6.50, 2.40)]  # 13
		]

class RedeNacionalPesquisa(Network): 
	""" Rede (Brasileira) Nacional de Pesquisa (Rede Ipê / RNP) """
	def __init__(self):
		super(RedeNacionalPesquisa, self).__init__()
		self.name        = 'RNP'
		self.fullname    = u'Rede Nacional de Pesquisas (Rede Ipê)'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

	def get_edges(self):
		""" get """
		return [\
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

	def get_nodes_2D_pos(self):
		""" Get position of the nodes on the bidimensional Cartesian plan
	
			This might be useful for plotting the topology as a undirected, 
			unweighted graph
		"""
		return [\
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

### EOF ###

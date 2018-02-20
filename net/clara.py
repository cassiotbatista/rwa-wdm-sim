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
# First version: Apr 2016
# Last edited on Feb 2018
#
# References:
# - random 'biased' choice: https://stackoverflow.com/q/25507558
# - import from parent dir: https://stackoverflow.com/a/30536516


class CooperacionLatinoAmericana(Network): 
	""" Cooperación Latino Americana de Redes Avanzadas (RedClara) """
	def __init__(self):
		super(CooperacionLatinoAmericana).__init__(self)
		self.name        = 'CLARA'
		self.fullname    = u'Cooperación Latino Americana de Redes Avanzadas'
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False FIXME
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

		self.block_count = 0
		self.block_list  = []

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

### EOF ###


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
# - import from parent dir: https://stackoverflow.com/a/30536516


class AdvancedResearchProjectsAgency(Network): 
	""" U.S. Advanced Research Projects Agency (ARPANET) """
	def __init__(self):
		super(AdvancedResearchProjectsAgency).__init__(self)
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

### EOF ###

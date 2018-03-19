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


class NationalScienceFoundation(Network): 
	""" U.S. National Science Foundation Network (NSFNET) """
	def __init__(self):
		super(NationalScienceFoundation).__init__(self)
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

### EOF ###

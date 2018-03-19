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


class RedeNacionalPesquisa(Network): 
	""" U.S. National Science Foundation Network (NSFNET) """
	def __init__(self):
		super(RedeNacionalPesquisa).__init__(self)
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

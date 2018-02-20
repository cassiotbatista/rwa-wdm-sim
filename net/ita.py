
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


class Italian(Network): 
	""" Italian Network (NSFNET) """
	def __init__(self):
		super(Italian).__init__(self)
		self.name        = 'ITA'
		self.fullname    = u''
		self.num_nodes   = len(self.get_nodes_2D_pos())
		self.num_links   = len(self.get_edges())

		# the below are used iff multi_SD is set to False
		self.source_node = 0   # source node defined for all connections
		self.dest_node   = 12  # destination node defined for all connections

		self.block_count = 0
		self.block_list  = []

	def get_edges(self):
		""" get """
		return [\
			(0,1), (0,2),							# 0
			(1,2), (1,3), (1,4),					# 1
			(2,7), (2,8), (2,9),					# 2
			(3,4), (3,5), 							# 3
			(4,6), (4,7),							# 4
			(5,6),									# 5
			(6,7),									# 6
			(7,9), (7,10),							# 7
			(8,9), (8,12),							# 8
			(9,11), (9,12),							# 9
			(10,13),								# 10
			(11,12), (11,13),						# 11
			(12,14), (12,20),						# 12
			(13,14), (13,15),						# 13
			(14,15), (14,16), (14,18), (14,19),		# 14
			(15,16),								# 15
			(16,17),								# 16
			(17,18),								# 17
			(18,19),								# 18
			(19,20)									# 19
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

### EOF ###

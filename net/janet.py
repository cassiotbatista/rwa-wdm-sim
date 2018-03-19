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


class JointAcademic(Network): 
	""" U.K. Joint Academic Network (JANET) """
	def __init__(self):
		super(JointAcademic).__init__(self)
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

### EOF ###

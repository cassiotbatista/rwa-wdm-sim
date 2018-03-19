#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA with Fixed Path routing (by Dijkstra's alg.) + First-Fit
# Routing with Dijkstra -> 1-Shortest Path
# Wavelength Assignment with First-Fit
#
# Authors: Apr 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last revised on Mar 2018
#
# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import info
import networkx as nx

class DijkstraFirstFit(RWAAlgorithm):
	def __init__(self):
		super(DijkstraFirstFit).__init__(self)
		self.name     = 'DFF'
		self.fullname = 'Dijkstra and First Fit'

	def routing(self, adj_mtx, source, destination):
		return self.dijkstra(adj_mtx, source, destination)

	def wavelength_assignment(self):
		return self.first_fit()

	def rwa(self, N, A, T, s, d, holding_time):
		""" This method RWAs """
		# call the routing method
		route = self.routing(A, s, d)

		# call the wavelength assignment method
		# TODO
		wavelength = self.wavelength_assignment(route, N, route, CHANNELS FIXME)

		if wavelength is not None:
			# if available on all links of R, alloc net resources for the call
			length = len(route)
			for r in xrange(length-1):
				rcurr = route[r]
				rnext = route[r+1]

				# make λ NOT available on all links of the path 
				# do not forget to make the wavelength matrix symmetrical
				N[rcurr][rnext][wavelength] = 0
				N[rnext][rcurr][wavelength] = N[rcurr][rnext][wavelength] # symm.
		
				# assign a time for it to be free again (released)
				# do not forget to make the traffic matrix symmetrical
				T[rcurr][rnext][wavelength] = holding_time
				T[rnext][rcurr][wavelength] = T[rcurr][rnext][wavelength] # symm.
	
			return 0 # allocated
		else:
			return 1 # block

### EOF ###

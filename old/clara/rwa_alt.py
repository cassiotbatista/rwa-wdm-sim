#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA with Fixed-Alternate Path + FF
# Routing with Yen -> K-Shortest Path 
# Wavelength Assignment with First-Fit
#
# Copyright 2017 Universidade Federal do Pará (PPGCC UFPA)
#
# Authors: Apr 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com

# Last revised on Apr 2017

# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks


import info
import networkx as nx

# https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.simple_paths.html
def yen(mat, (s,d), k):
	if any([s,d])<0 or any([s,d])>mat.shape[0] or k<0:
		print 'Error'
		return None
	G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
	paths = list(nx.shortest_simple_paths(G, s, d, weight=None))
	return paths[:k]

def get_wave_availability(k, n):
	return (int(n) & ( 1 << k )) >> k

def rwa_alt(N, A, T, holding_time):
	SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)

	# alternate k shortest paths
	routes = yen(A, SD, info.K)

	## GLOBAL KNOWLEDGE first fit wavelength assignment
	#color = None
	#for R in routes:
	#	avail = 2**info.NSF_NUM_CHANNELS-1
	#	for r in xrange(len(R)-1):
	#		rcurr = R[r]
	#		rnext = R[r+1]

	#		avail &= N[rcurr][rnext]

	#		if avail == 0:
	#			break

	#	if avail > 0:
	#		color = format(avail, '0%db' % info.NSF_NUM_CHANNELS)[::-1].index('1')
	#		break

	for R in routes:

		# LOCAL KNOWLEDGE first fit wavelength assignment
		color = None
		rcurr, rnext = R[0], R[1] # get the first two nodes from route R
		# Check whether each wavelength ...
		for w in xrange(info.NSF_NUM_CHANNELS):
			# ... is available on the first link of route R
			if get_wave_availability(w, N[rcurr][rnext]):
				color = w
				break

		if color is not None:
			# LOCAL KNOWLEDGE assure the color chosen at the first link is
			# availble on all links of the route R
			for r in xrange(len(R)-1):
				rcurr = R[r]
				rnext = R[r+1]

				# if not available in any of the next links, block
				if not get_wave_availability(color, N[rcurr][rnext]):
					color = None
					break # block for this route, give chance for the alternate

			if color is not None:
				# if available on all links of R, alloc net resources for the
				# call
				for r in xrange(len(R)-1):
					rcurr = R[r]
					rnext = R[r+1]

					N[rcurr][rnext] -= 2**color
					N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric
		
					T[rcurr][rnext][color] = holding_time
					T[rnext][rcurr][color] = T[rcurr][rnext][color]

				return 0 # allocated

	return 1 # blocked

### EOF ###

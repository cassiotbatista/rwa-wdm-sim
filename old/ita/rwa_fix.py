#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA with Fixed Path + FF
# Routing with Dijkstra -> 1-Shortest Path
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

# https://networkx.github.io/documentation/networkx-1.10/reference/algorithms.shortest_paths.html
def dijkstra(mat, (s,d)):
	if any([s,d])<0 or any([s,d])>mat.shape[0]:
		print 'Error'
		return None, None
	G = nx.from_numpy_matrix(mat, create_using=nx.Graph())
	hops, path = nx.bidirectional_dijkstra(G, s, d, weight=None)
	return path

def get_wave_availability(k, n):
	return (int(n) & ( 1 << k )) >> k

def rwa_fix(N, A, T, holding_time):
	SD = (info.NSF_SOURCE_NODE, info.NSF_DEST_NODE)
	R = dijkstra(A, SD)

	## GLOBAL KNOWLEDGE first fit wavelength assignment
	#color = None
	#avail = 2**info.NSF_NUM_CHANNELS-1
	#for r in xrange(len(R)-1):
	#	rcurr = R[r]
	#	rnext = R[r+1]

	#	avail &= N[rcurr][rnext]

	#	if avail == 0:
	#		break

	#	if avail > 0:
	#		color = format(avail, '0%db' % info.NSF_NUM_CHANNELS)[::-1].index('1')
	#		break
	
	# LOCAL KNOWLEDGE first fit wavelength assignment
	color = None
	rcurr, rnext = R[0], R[1]
	# Check whether each wavelength ...
	for w in xrange(info.NSF_NUM_CHANNELS):
		# ... is available on the first link of route R
		if get_wave_availability(w, N[rcurr][rnext]):
			color = w
			break

	if color is not None:
		# LOCAL KNOWLEDGE check if the color chosen at the first link is
		# availble on all links of the route R
		for r in xrange(len(R)-1):
			rcurr = R[r]
			rnext = R[r+1]

			# if not available in any of the next links, block
			if not get_wave_availability(color, N[rcurr][rnext]):
				return 1 # blocked

		# if available on all links of R, alloc net resources for the call
		for r in xrange(len(R)-1):
			rcurr = R[r]
			rnext = R[r+1]

			N[rcurr][rnext] -= 2**color
			N[rnext][rcurr] = N[rcurr][rnext] # make it symmetric
	
			T[rcurr][rnext][color] = holding_time
			T[rnext][rcurr][color] = T[rcurr][rnext][color]

		return 0 # allocated
	else:
		return 1 # blocked

#color = format(avail, '0%db' % info.NSF_NUM_CHANNELS)[::-1].index('1')
### EOF ###

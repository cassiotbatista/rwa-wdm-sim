#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA Simulator
# Routing and Wavelength Assignment with Static Traffic Simulator for
# All-Optical WDM Networks
#
# Author: April 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last revised on Apr 2018
#
# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks

import sys
sys.path.insert(0, 'src')

import os
import random
import numpy as np

# pretty-print a np array - https://stackoverflow.com/q/2891790
np.set_printoptions(precison=2)

from config import *
from net import *
from alg import *

# init all networks
def init_nets():
	nets = []
	if NET_ARPA:
		nets.append(AdvancedResearchProjectsAgency(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS)) 
	if NET_CLARA:
		nets.append(CooperacionLatinoAmericana(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS))
	if NET_ITA:
		nets.append(Italian(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS))
	if NET_JANET:
		nets.append(JointAcademic(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS))
	if NET_NSF:
		nets.append(NationalScienceFoundation(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS))
	if NET_RNP:
		nets.append(RedeNacionalPesquisa(NET_NUM_CHANNELS,
				NET_CHANNEL_FREE, NET_CHANNEL_BIAS))

	return nets

# init all algorithms
def init_algs():
	algs = []
	if ALG_DFF:
		algs.append(DijkstraFirstFit())         # 0 DFF
	if ALG_DGC:
		algs.append(DijkstraGraphColoring())    # 1 GGC
	if ALG_YFF:
		algs.append(YenFirstFit(YEN_K))         # 2 YFF
	if ALG_YGC:
		algs.append(YenGraphColoring(YEN_K))    # 3 YGC
	if ALG_GA: # FIXME I need to pass some args from config.py here
		algs.append(GeneticAlgorithm())         # 4 GA
	if ALG_GOF:
		algs.append(GeneralObjectiveFunction()) # 5 GOF (alone)

	return algs

def poisson_arrival():
	r = np.random.uniform() # half-open interval [low=0.0, high=1.0)
	while r == 0.0 or r == 1.0: # I better be sure, right?
		r = np.random.uniform()
	return -np.log(1-r)

def gen_od_pair(net)
	if not net.allow_multi_od:
		return net.source_node, net.dest_node

	# randomly choose origin and destination nodes
	origin      = random.randrange(net.num_nodes) 
	destination = random.randrange(net.num_nodes)

	# avoid origin node being the same as destination
	while origin == destination:
		destination = random.randrange(net.num_nodes) 

	return origin, destination

def main():
	nets = init_nets()
	algs = init_algs()

	if nets == [] or algs == []:
		sys.stderr.write('Something must be wrong. ')
		sys.stderr.write('You didn\'t start any network [n]or algorithm.\n')
		sys.stderr.write('Take a look at NET_* or ALG_* consts in \'info.py\'.')
		sys.stderr.flush()
		sys.exit(1)

	# init the block array for each topology, considerind each and every node of
	# the topology as an eventual origin node
	for n in nets:
		n.init_network()
		for a in algs:
			a.block_dict[n.name] = {}
			for node in range(n.num_nodes):              # e.g.: cur node = 2
				a.block_count.append(0)                  # list[2]        = 0
				a.block_dict[n.name][node] = np.empty(0) # dict['nsf'][2] = 0.0

	# define the load in Erlangs
	for load in xrange(SIM_MIN_LOAD, SIM_MAX_LOAD):
		# reset all networks to the inital state
		for n in nets:
			n.reset_network()

		# call requests arrival
		for call in xrange(SIM_NUM_CALLS):
			# exponential time distributions
			holding_time = poisson_arrival() # define a time for a λ to be released
			until_next   = poisson_arrival()/load # define interarrival times

			# FIXME apply RWA
			for n in nets:
				o, d = gen_od_pair(n)
				for a in algs:
					a.block_count[o] += a.rwa(n, o, d, holding_time)

			if DEGUB:
				sys.stdout.write('\rLoad: %2d/%2d Simul: %4d/%4d\t' % (load,
						SIM_MAX_LOAD-1, call+1, SIM_NUM_CALLS))
				for a in algs:
					sys.stdout.write('%6s:  %5d, '  % (a.name, a.block_count))
				sys.stdout.flush()

			# update networks
			for n in nets:
				n.update_network(until_next)
		# exits Poisson for (call) loop

		# save % BP per load (partial BP per erlang. max=100%)
		for n in nets:
			for a in algs:
				a.save_erlang_blocks(n.name, n.num_nodes, SIM_NUM_CALLS)
		print 'Done'
	# exits Erlang for (load) loop

	# FIXME
	if DEGUB:
		for n in nets:
			for a in algs:
				print '\t%6s %s' % (a.name, a.block_dict)

	# save BPs to file
	for n in nets:
		for a in algs:
			a.save_blocks_to_file(RESULT_DIR, n.name, n.num_nodes, NET_NUM_CHANNELS)

if __name__ == '__main__':
	main()

### EOF ###

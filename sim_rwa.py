#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm: 
# Routing and Wavelength Assignment with General Objective Function
#
# Authors: April 2017
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
sys.path.insert(0, 'net')
sys.path.insert(0, 'src')

import os

import random
import numpy as np

import info import *

from arpa import AdvancedResearchProjectsAgency
from clara import CooperacionLatinoAmericana
from ita import Italian
from nsf import NationalScienceFoundation
from rnp import RedeNacionalPesquisa

def poisson_arrival():
	r = np.random.uniform() # half-open interval [low=0.0, high=1.0)
	while r == 0.0 or r == 1.0: # I better be sure, right?
		r = np.random.uniform()
	return -np.log(1-r)

# init all nets
def init_nets():
	nets = []
	nets.append(AdvancedResearchProjectsAgency()) # 0 ARPA
	nets.append(CooperacionLatinoAmericana())     # 1 CLARA
	nets.append(Italian())                        # 3 ITALIAN
	nets.append(JointAcademic())                  # 4 JANET
	nets.append(NationalScienceFoundation())      # 5 NSF
	nets.append(RedeNacionalPesquisa())           # 6 RNP

	return nets

# init all algs
def init_algs():
	algs = []
	algs.append(DijkstraFirstFit())         # 0 DFF
	algs.append(DijkstraGraphColoring())    # 1 GGC
	algs.append(YenFirstFit())              # 2 YFF
	algs.append(YenGraphColoring())         # 3 YGC
	algs.append(GeneticAlgorithm())         # 4 GA
	algs.append(GeneralObjectiveFunction()) # 5 GOF (alone)

	return algs

def main():

	nets = init_nets()
	algs = init_algs()

	for n in nets:
		n.init_network()
		for a in algs:
			a.block_dict[n.name] = {}

	for load in xrange(info.SIM_MIN_LOAD, info.SIM_MAX_LOAD):
		for n in nets:
			n.reset_network()

		for call in xrange(info.SIM_NUM_CALLS):
			holding_time = poisson_arrival() # define a time for a λ to be released
			until_next   = poisson_arrival()/load # define interarrival times

			for n in nets:
				for a in algs:
					a.block_count += a.rwa(n, holding_time, until_next)

			if info.DEGUB:
				sys.stdout.write('\r')
				sys.stdout.write('Load: %2d/%2d '   % (load, info.SIM_MAX_LOAD-1))
				sys.stdout.write('Simul: %4d/%4d\t' % (call+1, info.SIM_NUM_CALLS))
				for a in algs:
					sys.stdout.write('%3s:  %4d, '  % (a.name, a.block_count))
				sys.stdout.flush()

		for a in algs:
			a.block_list.append(100.0*a.block_count/info.SIM_NUM_CALLS)
		print 'Done'

	if info.DEGUB:
		for a in algs:
			print '\t %3s %s' % (a.name, a.block_list)

	for a in algs:
		a.save_blocks_to_file()
		with open('block_%s_%d.txt' % (a.name,info.NSF_NUM_CHANNELS)) as f:
			text = re.sub(r'[\[\]]', '', str(a.block_list)))
			f.write('%s; ...\n' % text)

if __name__ == '__main__':
	main()

### EOF ###

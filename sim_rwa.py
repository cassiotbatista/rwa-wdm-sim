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

import info
import nsf

import numpy as np

from rwa_ga import rwa_ga

from rwa_dij_gc import rwa_dij_gc
from rwa_yen_gc import rwa_yen_gc

from rwa_yen_ff import rwa_yen_ff
from rwa_dij_ff import rwa_dij_ff

if __name__ == '__main__':

	# init all nets
	nets = []
	nets.append(AdvancedResearchProjectsAgency()) # 0 ARPA
	nets.append(CooperacionLatinoAmericana())     # 1 CLARA
	nets.append(Italian())                        # 3 ITALIAN
	nets.append(JointAcademic())                  # 4 JANET
	nets.append(NationalScienceFoundation())      # 5 NSF
	nets.append(RedeNacionalPesquisa())           # 6 RNP

	for n in nets:
		n.init_network()

	algs = []
	algs.append(DijkstraFirstFit())         # 0 DFF
	algs.append(DijkstraGraphColoring())    # 1 GGC
	algs.append(YenFirstFit())              # 2 YFF
	algs.append(YenGraphColoring())         # 3 YGC
	algs.append(GeneticAlgorithm())         # 4 GA
	algs.append(GeneralObjectiveFunction()) # 5 GOF (alone)

	if info.DEBUG:
		print nsf_wave

	for load in xrange(info.SIM_MIN_LOAD, info.SIM_MAX_LOAD):
		for n in nets:
			n.reset_network()

		for call in xrange(info.SIM_NUM_GEN):
			r = np.random.uniform() # half-open interval [low=0.0, high=1.0)
			while r == 0.0 or r == 1.0: # I better be sure, right?
				r = np.random.uniform()
			until_next = -np.log(1-r)/load # define interarrival times

			r = np.random.uniform() # half-open interval [low=0.0, high=1.0)
			while r == 0.0 or r == 1.0: # I better be sure, right?
				r = np.random.uniform()
			holding_time = -np.log(1-r) # define a time for a λ to be released

			for n in nets:
				for a in algs:
					a.block_count += a.rwa(n, holding_time, until_next)

			if info.DEBUG:
				sys.stdout.write('\r')
				sys.stdout.write('Load: %2d/%2d '   % (load, info.SIM_MAX_LOAD-1))
				sys.stdout.write('Simul: %4d/%4d\t' % (call+1, info.SIM_NUM_GEN))
				for a in algs:
					sys.stdout.write('%3s:  %4d, '    % (a.name, a.block_count))
				sys.stdout.flush()

		blocked_ga.append( 100.0*count_block_ga /info.SIM_NUM_GEN)
		blocked_dij_gc.append(100.0*count_block_dij_gc/info.SIM_NUM_GEN)
		blocked_yen_gc.append(100.0*count_block_yen_gc/info.SIM_NUM_GEN)
		blocked_yen_ff.append(100.0*count_block_yen_ff/info.SIM_NUM_GEN)
		blocked_dij_ff.append(100.0*count_block_dij_ff/info.SIM_NUM_GEN)
		print 'Done'

	if info.DEBUG:
		for a in algs:
			print '\t %3s %s' % (a.name, a.block_list)
	
	with open('block_GA_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_ga).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_DIJ_gc_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_dij_gc).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_YEN_gc_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_yen_gc).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_YEN_FF_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_yen_ff).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_DIJ_FF_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_dij_ff).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)

### EOF ###

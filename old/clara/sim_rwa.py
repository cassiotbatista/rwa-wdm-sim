#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm: 
# Routing and Wavelength Assignment with General Objective Function
#
# Copyright 2017 Universidade Federal do Pará (PPGCC UFPA)
#
# Authors: April 2017
# Cassio Trindade Batista - cassio.batista.13@gmail.com

# Last revised on Apr 2017

# REFERENCES:
# [1] 
# Afonso Jorge F. Cardoso et. al., 2010
# A New Proposal of an Efficient Algorithm for Routing and Wavelength 
# Assignment (RWA) in Optical Networks

import sys

import info
import nsf

import numpy as np

from rwa_ga import rwa_ga

from rwa_std_fix import rwa_std_fix
from rwa_std_alt import rwa_std_alt

from rwa_alt import rwa_alt
from rwa_fix import rwa_fix

def get_wave_availability(k, n):
	return (int(n) & ( 1 << k )) >> k

if __name__ == '__main__':

	nsf_wave, nsf_adj, nsf_time, nsf_links = nsf.generate()

	blocked_ga  = []
	blocked_std_fix = []
	blocked_std_alt = []
	blocked_alt = []
	blocked_fix = []

	if info.DEBUG:
		print nsf_wave

	for load in xrange(info.SIM_MIN_LOAD, info.SIM_MAX_LOAD):
		N_ga  = nsf_wave.copy()
		N_std_fix = nsf_wave.copy()
		N_std_alt = nsf_wave.copy()
		N_alt = nsf_wave.copy()
		N_fix = nsf_wave.copy()

		T_ga  = nsf_time.copy() # holding time
		T_std_fix = nsf_time.copy() # holding time
		T_std_alt = nsf_time.copy() # holding time
		T_alt = nsf_time.copy() # holding time
		T_fix = nsf_time.copy() # holding time
	
		paths_fix = []
		paths_alt = []

		count_block_ga  = 0
		count_block_std_fix = 0
		count_block_std_alt = 0
		count_block_alt = 0
		count_block_fix = 0

		for gen in xrange(info.SIM_NUM_GEN):
			until_next   = -np.log(1-np.random.rand())/load
			holding_time = -np.log(1-np.random.rand())
	
			count_block_ga  += rwa_ga(N_ga,  nsf_adj, T_ga,  holding_time)
			count_block_std_fix += rwa_std_fix(N_std_fix, nsf_adj, T_std_fix, holding_time, paths_fix)
			count_block_std_alt += rwa_std_alt(N_std_alt, nsf_adj, T_std_alt, holding_time, paths_alt)
			count_block_alt += rwa_alt(N_alt, nsf_adj, T_alt, holding_time)
			count_block_fix += rwa_fix(N_fix, nsf_adj, T_fix, holding_time)

			if info.DEBUG:
				sys.stdout.write('\rLoad: %02d/%02d ' % (load, info.SIM_MAX_LOAD-1))
				sys.stdout.write('Simul: %04d/%04d\t' % (gen+1, info.SIM_NUM_GEN))
				sys.stdout.write('GA:  %04d, ' % count_block_ga)
				sys.stdout.write('STF: %04d, ' % count_block_std_fix)
				sys.stdout.write('STA: %04d, ' % count_block_std_alt)
				sys.stdout.write('ALT: %04d, ' % count_block_alt)
				sys.stdout.write('FIX: %04d '  % count_block_fix)
				sys.stdout.flush()
	
			aux_fix = {idx:[] for idx in xrange(info.NSF_NUM_CHANNELS)}
			aux_alt = {idx:[] for idx in xrange(info.NSF_NUM_CHANNELS)}
			# Atualiza os todos os canais que ainda estao sendo usados 
			for link in nsf_links:
				i, j = link
				for w in xrange(info.NSF_NUM_CHANNELS):

					# GA + GOF
					if  T_ga[i][j][w] > until_next:
						T_ga[i][j][w] -= until_next
						T_ga[j][i][w]  = T_ga[i][j][w]
					else:
						T_ga[i][j][w] = 0
						T_ga[j][i][w] = 0
						if not get_wave_availability(w, N_ga[i][j]):
							N_ga[i][j] += 2**w # free channel
							N_ga[j][i] = N_ga[i][j] 

					# Dijkstra + Graph coloring
					if  T_std_fix[i][j][w] > until_next:
						T_std_fix[i][j][w] -= until_next
						T_std_fix[j][i][w]  = T_std_fix[i][j][w]
					else:
						T_std_fix[i][j][w] = 0
						T_std_fix[j][i][w] = 0
						if not get_wave_availability(w, N_std_fix[i][j]):
							N_std_fix[i][j] += 2**w # free channel
							N_std_fix[j][i] = N_std_fix[i][j] 
							aux_fix[w].append((i,j))
							aux_fix[w].append((j,i))

					# Yen + Graph coloring
					if  T_std_alt[i][j][w] > until_next:
						T_std_alt[i][j][w] -= until_next
						T_std_alt[j][i][w]  = T_std_alt[i][j][w]
					else:
						T_std_alt[i][j][w] = 0
						T_std_alt[j][i][w] = 0
						if not get_wave_availability(w, N_std_alt[i][j]):
							N_std_alt[i][j] += 2**w # free channel
							N_std_alt[j][i] = N_std_alt[i][j] 
							aux_alt[w].append((i,j))
							aux_alt[w].append((j,i))

					# Yen + First-fit
					if  T_alt[i][j][w] > until_next:
						T_alt[i][j][w] -= until_next
						T_alt[j][i][w]  = T_alt[i][j][w]
					else:
						T_alt[i][j][w] = 0
						T_alt[j][i][w] = 0
						if not get_wave_availability(w, N_alt[i][j]):
							N_alt[i][j] += 2**w # free channel
							N_alt[j][i] = N_alt[i][j] 

					# Dijkstra + First-fit
					if  T_fix[i][j][w] > until_next:
						T_fix[i][j][w] -= until_next
						T_fix[j][i][w]  = T_fix[i][j][w]
					else:
						T_fix[i][j][w] = 0
						T_fix[j][i][w] = 0
						if not get_wave_availability(w, N_fix[i][j]):
							N_fix[i][j] += 2**w # free channel
							N_fix[j][i] = N_fix[i][j] 

			pop_fix = []
			for path in paths_fix:
				R, color = path
				count = 0
				if color == None:
					continue
				for r in xrange(len(R)-1):
					rcurr = R[r]
					rnext = R[r+1]
					if (rcurr,rnext) in aux_fix[color]:
						count += 1
				if count == len(R)-1:
					pop_fix.append(paths_fix.index(path))

			pop_fix.sort() # make sure the last elements are popped first
			while len(pop_fix):
				paths_fix.pop(pop_fix.pop())

			pop_alt = []
			for path in paths_alt:
				R, color = path
				count = 0
				if color == None:
					continue
				for r in xrange(len(R)-1):
					rcurr = R[r]
					rnext = R[r+1]
					if (rcurr,rnext) in aux_alt[color]:
						count += 1
				if count == len(R)-1:
					pop_alt.append(paths_alt.index(path))

			pop_alt.sort() # make sure the last elements are popped first
			while len(pop_alt):
				paths_alt.pop(pop_alt.pop())

		blocked_ga.append( 100.0*count_block_ga /info.SIM_NUM_GEN)
		blocked_std_fix.append(100.0*count_block_std_fix/info.SIM_NUM_GEN)
		blocked_std_alt.append(100.0*count_block_std_alt/info.SIM_NUM_GEN)
		blocked_alt.append(100.0*count_block_alt/info.SIM_NUM_GEN)
		blocked_fix.append(100.0*count_block_fix/info.SIM_NUM_GEN)
		print 'Done'

	if info.DEBUG:
		print '\tGA:  ', blocked_ga
		print '\tSTF: ', blocked_std_fix
		print '\tSTA: ', blocked_std_alt
		print '\tALT: ', blocked_alt
		print '\tFIX: ', blocked_fix
	
	with open('block_GA_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_ga).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_STF_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_std_fix).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_STA_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_std_alt).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_ALT_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_alt).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)
	
	with open('block_FIX_%d.m' % info.NSF_NUM_CHANNELS, 'a') as f:
		text = str(blocked_fix).replace('[','').replace(']','')
		f.write('%s; ...\n' % text)

### EOF ###

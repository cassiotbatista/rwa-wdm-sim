#!/usr/bin/env python2
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# RWA Simulator
# Routing and Wavelength Assignment with Static Traffic Simulator for
# All-Optical WDM Networks
#
# Author: Apr 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
# Federal University of Pará (UFPA). Belém, Brazil.
#
# Last revised on Mar, 2018

import os

# Debug Parameters
DEBUG = False

RESULT_DIR = os.path.join(os.path.abspath(__file__), 'results')

# Simulation Parameters
SIM_NUM_CALLS = 150
SIM_MIN_LOAD  = 1
SIM_MAX_LOAD  = 31

# NET Parameters
NET_NUM_CHANNELS  = 4      # total number of wavelengths available
NET_CHANNEL_FREE  = False  # init all link wavelengths available at once?
NET_CHANNEL_BIAS  = 0.50   # probability of free λ vs occupied λ, respect.

NET_ARPA   = True  # use ARPA    network topology in simulation?
NET_CLARA  = True  # use CLARA   network topology in simulation?
NET_ITA    = True  # use ITALIAN network topology in simulation?
NET_JANET  = True  # use JANET   network topology in simulation?
NET_RNP    = True  # use RNP     network topology in simulation?
NET_NSF    = True  # use NSF     network topology in simulation?

ALG_DFF    = True  # use 'Dijkstra + First Fit'       algoritihms in simulation?    
ALG_DGC    = True  # use 'Dijkstra + Graph Coloring'  algoritihms in simulation?    
ALG_YFF    = True  # use 'Yen + First Fit'            algoritihms in simulation?    
ALG_YGC    = True  # use 'Yen + Graph Coloring'       algoritihms in simulation?    
ALG_GA     = True  # use 'Genetic Algorithm'                      in simulation?    
ALG_GOF    = True  # use 'General Objective Function' algoritihm  in simulation?    

# TODO: pass everything as a dict to the class
# GA Parameters
GA_SIZE_POP       = 30     # size of the population of each species

GA_MIN_GEN        = 25     # min number of generations
GA_MAX_GEN        = 80     # max number of generations

GA_MIN_CROSS_RATE = 0.15   # min crossover rate
GA_MAX_CROSS_RATE = 0.40   # max crossover rate

GA_MIN_MUT_RATE   = 0.02   # min mutation rate
GA_MAX_MUT_RATE   = 0.20   # max mutation rate

GA_GEN_INTERVAL   = 8      # interval to update rates

# Yen's Algorithm Parameters
YEN_K = 2

### EOF ###

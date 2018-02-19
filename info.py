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
# Last edited on Feb, 2018


# Debug Parameters
DEBUG = False

# Simulation Parameters
SIM_NUM_GEN = 150

SIM_MIN_LOAD = 1
SIM_MAX_LOAD = 31

# NSF Parameters
NSF_SOURCE_NODE   = 0      # source
NSF_DEST_NODE     = 12     # destination node
NSF_NUM_NODES     = 14     # number of nodes on NSF network

NSF_NUM_CHANNELS  = 4      # total number of wavelengths available
NSF_CHANNEL_FREE  = False  # init all link wavelengths available at once?
NSF_CHANNEL_BIAS  = [0.50, 0.50]  # probability of free wl vs occupied wl, respect.

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
K = 2

### EOF ###

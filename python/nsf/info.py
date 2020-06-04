#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# vim: set fileencoding=utf-8
#
# GA: RWA with GOF
# Genetic Algorithm  
# Routing and Wavelength Assignment
# General Objective Function
#
# Copyright 2017
# Programa de Pós-Graduação em Ciência da Computação (PPGCC)
# Universidade Federal do Pará (UFPA)
#
# Author: April 2016
# Cassio Trindade Batista - cassio.batista.13@gmail.com
#
# Last edited on June, 2020

# Debug Parameters
DEBUG = True
RESULTS_DIR = './results'
PLOT_RESULTS = True

# Simulation Parameters
SIM_NUM_GEN = 150         # this represents the number of calls (connection
                          # requests) arriving at the system to be either
                          # attended of blocked by our RWA algorithms

SIM_MIN_LOAD = 1          # first Erlang value (closed interval)
SIM_MAX_LOAD = 21         # last Erlang value (open interval)

# NSF Parameters
NSF_SOURCE_NODE  = 0      # source for all cals
NSF_DEST_NODE    = 12     # destination node
NSF_NUM_NODES    = 14     # number of nodes on NSF network

NSF_NUM_CHANNELS = 8      # total number of wavelengths available
NSF_CHANNEL_FREE = False  # init all link wavelengths available at once?

# Genetic Algorithm Parameters
GA_SIZE_POP       = 30    # size of the population of each species

GA_MIN_GEN        = 25    # min number of generations
GA_MAX_GEN        = 80    # max number of generations

GA_MIN_CROSS_RATE = 0.15  # min crossover rate
GA_MAX_CROSS_RATE = 0.40  # max crossover rate

GA_MIN_MUT_RATE   = 0.02  # min mutation rate
GA_MAX_MUT_RATE   = 0.20  # max mutation rate

# Yen's Algorithm Parameters
K = 2

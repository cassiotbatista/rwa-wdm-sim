/*
 * GA: RWA with GOF
 * Genetic Algorithm  
 * Routing and Wavelength Assignment
 * General Objective Function
 *
 * Copyright 2017
 * Programa de Pós-Graduação em Ciência da Computação (PPGCC)
 * Universidade Federal do Pará (UFPA)
 *
 * Author: July 2017
 * Cassio Trindade Batista - cassio.batista.13@gmail.com
 *
 * Last edited on July, 2017
 */

#ifndef INFO_H_
#define INFO_H_

/* **************** */
/* Debug Parameters */
/* **************** */
#define DEBUG 1

/* ********************* */
/* Simulation Parameters */
/* ********************* */
#define SIM_NUM_GEN 1

#define SIM_MIN_LOAD 1
#define SIM_MAX_LOAD 11

/* ************** */
/* NSF Parameters */
/* ************** */
#define NSF_SOURCE_NODE   0     // source node
#define NSF_DEST_NODE     12    // destination node

#define NSF_NUM_NODES     14    // number of nodes on NSF network
#define NSF_NUM_CHANNELS  8    // total number of wavelengths available
#define NSF_CHANNEL_FREE  0     // init all link wavelengths available at once?

/* **************************** */
/* Genetic Algorithm Parameters */
/* **************************** */
#define GA_SIZE_POP       10    // size of the population of each species

#define GA_MIN_GEN        5    // min number of generations
#define GA_MAX_GEN        40    // max number of generations

#define GA_MIN_CROSS_RATE 0.15  // min crossover rate
#define GA_MAX_CROSS_RATE 0.40  // max crossover rate

#define GA_MIN_MUT_RATE   0.02  // min mutation rate
#define GA_MAX_MUT_RATE   0.20  // max mutation rate

#define GA_GEN_INTERVAL   8     // interval to update rates

#endif
/*** EOF ***/ 

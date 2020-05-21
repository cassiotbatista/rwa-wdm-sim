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

// https://stackoverflow.com/questions/7109964/creating-your-own-header-file-in-c
// https://stackoverflow.com/questions/20120833/how-do-i-refer-to-a-typedef-in-a-header-file

#ifndef RWA_GA_H_
#define RWA_GA_H_

#include "list.h"
#include "nsf.h"

typedef struct individual {
	node* R;
	bool* L;
	int chn_free;
	int length;
} individual;

typedef struct couple {
	individual* male;
	individual* female;
} couple;

bool         make_chromosome(nsf*, individual*, int, int);
individual*  _mutate(nsf* nsf_net, individual* chrom_normal);
int*         _select(individual **population, int k, int *pop_idxs);
couple*      _cross(individual *father, individual *mother);
individual*  evaluate(individual* ind, nsf* N);
void         insertion_sort(individual **pop, int size);
void         individual_free(individual *ind);
int          rwa(nsf **G, float holding_time);

#endif
/*** EOF ***/

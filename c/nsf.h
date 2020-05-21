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

#ifndef NSF_H_
#define NSF_H_

#include <stdbool.h>

typedef struct nsf {
	int i; // 1st-D
	int j; // 2nd-D
	int w; // 3rd-D

	bool**   A; // adjacency matrix
	bool***  N; // wavelength availability
	float*** T; // traffix time matrix
} nsf;

nsf* nsf_generate(nsf* nsf_net);
void nsf_free(nsf* nsf_net);
nsf* nsf_deep_copy(nsf* nsf_origin, nsf* nsf_copy);

#endif
/*** EOF ***/

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

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "info.h"
#include "nsf.h"

nsf*
nsf_generate(nsf* nsfpack)
{
	//if(nsfpack == NULL) {
	//	fprintf(stderr, "A memória deve ser alocada antes!\n");
	//	return NULL;
	//}

	int i, j, w;

	/* define number of rows and columns of all matrixes */
	nsfpack->i = nsfpack->j = NSF_NUM_NODES;

	/* define the number of wavelengths per fiber link */
	nsfpack->w = NSF_NUM_CHANNELS;

	/* allocate memory for adjacency matrix */
	nsfpack->A = malloc(nsfpack->i * sizeof(bool*));
	for(i=0; i<nsfpack->i; i++)
		nsfpack->A[i] = (bool*)calloc(nsfpack->i, sizeof(bool));

	/* allocate memory for wavelength matrix */
	nsfpack->N = (bool***)malloc(nsfpack->i * sizeof(bool**));
	for(i=0; i<nsfpack->i; i++) {
		nsfpack->N[i] = (bool**)malloc(nsfpack->i * sizeof(bool*));
		for(j=0; j<nsfpack->j; j++) {
			nsfpack->N[i][j] = (bool*)calloc(nsfpack->i, sizeof(bool));
		}
	}

	/* allocate memory for traffix time matrix */
	nsfpack->T = (float***)malloc(nsfpack->i * sizeof(float**));
	for(i=0; i<nsfpack->i; i++) {
		nsfpack->T[i] = (float**)malloc(nsfpack->i * sizeof(float*));
		for(j=0; j<nsfpack->j; j++) {
			nsfpack->T[i][j] = (float*)calloc(nsfpack->i, sizeof(float));
		}
	}

	/* fill adjacency matrix with one-way (directed) edges */
	nsfpack->A[0][1]   = nsfpack->A[0][2]   = nsfpack->A[0][5]  = 1; // 0
	nsfpack->A[1][2]   = nsfpack->A[1][3]   = 1;                     // 1
	nsfpack->A[2][8]   = 1;                                          // 2
	nsfpack->A[3][4]   = nsfpack->A[3][6]   = nsfpack->A[3][13] = 1; // 3
	nsfpack->A[4][9]   = 1;                                          // 4
	nsfpack->A[5][6]   = nsfpack->A[5][10]  = 1;                     // 5
	nsfpack->A[6][7]   = 1;                                          // 6
	nsfpack->A[7][8]   = 1;                                          // 7
	nsfpack->A[8][9]   = 1;                                          // 8
	nsfpack->A[9][11]  = nsfpack->A[9][12]  = 1;                     // 9
	nsfpack->A[10][11] = nsfpack->A[10][12] = 1;                     // 10
	nsfpack->A[11][13] = 1;                                          // 11

	/* make adjacency matrix symmetrical: two-way edges (undirected graph) */
	for(i=0; i<nsfpack->i; i++) {
		for(j=i+1; j<nsfpack->j; j++) {
			if(nsfpack->A[i][j]) {
				nsfpack->A[j][i] = nsfpack->A[i][j];
			}
		}
	}

	/* fill wavelength availability and traffic matrix */
	bool wavail;
	for(i=0; i<nsfpack->i; i++) {
		for(j=i+1; j<nsfpack->j; j++) {
			if(nsfpack->A[i][j]) {
				for(w=0; w<nsfpack->w; w++) {
					wavail = (bool) (rand() % 2);
					nsfpack->N[i][j][w] = nsfpack->N[j][i][w] = wavail;
					if(wavail)
						nsfpack->T[i][j][w] = nsfpack->T[j][i][w] = rand()/(float)RAND_MAX;
				}
			}
		}
	}

	return nsfpack;
}

void
nsf_free(nsf* nsf_net)
{
	int i, j; 
	for(i=0; i<nsf_net->i; i++) {
		/* free lowest level of 3D arrays first */
		for(j=0; j<nsf_net->j; j++) {
			free(nsf_net->N[i][j]);
			free(nsf_net->T[i][j]);
		}

		/* free the second level (rows) */
		free(nsf_net->N[i]);
		free(nsf_net->A[i]);
		free(nsf_net->T[i]);
	}

	/* free the whole data structure */
	free(nsf_net->N);
	free(nsf_net->A);
	free(nsf_net->T);

	free(nsf_net);
}

// http://courses.cs.vt.edu/~cs2505/fall2010/Notes/pdf/T30.CDeepCopy.pdf
nsf*
nsf_deep_copy(nsf* nsf_origin, nsf* nsf_copy) 
{
	//if(nsf_origin->A==NULL || nsf_origin->N==NULL || nsf_origin->T==NULL || 
	//   nsf_copy->A == NULL || nsf_copy->N == NULL || nsf_copy->T == NULL) {
	//	fprintf(stderr, "NSF structures must not be empty!\n");
	//	return NULL;
	//}

	int i, j, w;

	/* copy matrices numbers of rows and columns and number of wavelengths per link */
	nsf_copy->i = nsf_origin->i;
	nsf_copy->j = nsf_origin->j;
	nsf_copy->w = nsf_origin->w;

	/* allocate memory for adjacency matrix */
	nsf_copy->A = (bool**)malloc(nsf_copy->i * sizeof(bool*));
	for(i=0; i<nsf_copy->i; i++)
		nsf_copy->A[i] = (bool*)calloc(nsf_copy->i, sizeof(bool));

	/* allocate memory for wavelength matrix */
	nsf_copy->N = (bool***)malloc(nsf_copy->i * sizeof(bool**));
	for(i=0; i<nsf_copy->i; i++) {
		nsf_copy->N[i] = (bool**)malloc(nsf_copy->i * sizeof(bool*));
		for(j=0; j<nsf_copy->j; j++)
			nsf_copy->N[i][j] = (bool*)calloc(nsf_copy->i, sizeof(bool));
	}

	/* allocate memory for traffix time matrix */
	nsf_copy->T = (float***)malloc(nsf_copy->i * sizeof(float**));
	for(i=0; i<nsf_copy->i; i++) {
		nsf_copy->T[i] = (float**)malloc(nsf_copy->i * sizeof(float*));
		for(j=0; j<nsf_copy->j; j++)
			nsf_copy->T[i][j] = (float*)calloc(nsf_copy->i, sizeof(float));
	}

	/* copy adjacency, wavelength availability and traffic matrices */
	for(i=0; i<nsf_origin->i; i++) {
		for(j=i+1; j<nsf_origin->j; j++) {
			if(nsf_origin->A[i][j]) {
				nsf_copy->A[i][j] = nsf_copy->A[j][i] = nsf_origin->A[i][j];
				for(w=0; w<nsf_origin->w; w++) {
					nsf_copy->N[i][j][w] = nsf_copy->N[j][i][w] = nsf_origin->N[i][j][w];
					nsf_copy->T[i][j][w] = nsf_copy->T[j][i][w] = nsf_origin->T[i][j][w];
				}
			}
		}
	}

	return nsf_copy;
}

/*** EOF ***/

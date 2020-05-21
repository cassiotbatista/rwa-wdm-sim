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
#include <unistd.h>
#include <time.h>
#include <math.h>

#include "info.h"
#include "list.h"
#include "nsf.h"
#include "rwa_ga.h"

// https://stackoverflow.com/questions/2438142/dynamic-memory-allocation-for-3d-array
// https://stackoverflow.com/questions/2128728/allocate-matrix-in-c
// https://stackoverflow.com/questions/1694827/random-float-number
// https://stackoverflow.com/questions/7109964/creating-your-own-header-file-in-c

int
main(int argc, char** argv)
{
	int i, j, w; 
	int load, gen;
	
	float until_next, holding_time;
	int count_block;

	nsf* nsfpack;
	nsf* nsf_net;

	FILE* fp = NULL;
	if(!(fp = fopen("block.txt", "w"))) {
		printf("Failed to open block file\n");
		exit(0);
	}

	srand(time(NULL));

	/* init NSF network data structure */
	nsfpack = (nsf*)malloc(sizeof(nsf));
	nsfpack = nsf_generate(nsfpack);

	for(load=SIM_MIN_LOAD; load<SIM_MAX_LOAD; load++) {
		nsf_net = (nsf*)malloc(sizeof(nsf));
		nsf_net = nsf_deep_copy(nsfpack, nsf_net);

		count_block = 0;

		for(gen=0; gen<SIM_NUM_GEN; gen++) {
			until_next   = -logf(1-(rand()/(float)RAND_MAX))/load;
			holding_time = -logf(1-(rand()/(float)RAND_MAX));

			printf("before:\n");
			for(j=0; j<nsf_net->j; j++) {
				for(w=0; w<nsf_net->w; w++) {
					printf("%d ", nsf_net->N[0][j][w]);
				}
				printf("\n");
			}

			count_block += rwa(&nsf_net, holding_time);

			printf("after:\n");
			for(j=0; j<nsf_net->j; j++) {
				for(w=0; w<nsf_net->w; w++) {
					printf("%d ", nsf_net->N[0][j][w]);
				}
				printf("\n");
			}

			if(!DEBUG) {
				printf("\rLoad: %02d/%02d ", load, SIM_MAX_LOAD-1);
				printf("Simul: %04d/%04d\t", gen+1, SIM_NUM_GEN);
				printf("GA:  %04d, ", count_block);
			}

			// Atualiza os todos os canais que ainda estao sendo usados */
			for(i=0; i<NSF_NUM_NODES; i++) {
				for(j=i+1; j<NSF_NUM_NODES; j++) {
					if(!nsf_net->A[i][j]) // if there's no adjacency, try another node
						continue;

					for(w=0; w<NSF_NUM_CHANNELS; w++) {
						if(nsf_net->T[i][j][w] > until_next) {
							nsf_net->T[i][j][w] = nsf_net->T[j][i][w] -= until_next;
						} else {
							nsf_net->T[i][j][w] = nsf_net->T[j][i][w] = 0.0;

							/* if channel is still busy, set it free */
							if(!nsf_net->N[i][j][w]) 
								nsf_net->N[i][j][w] = nsf_net->N[j][i][w] = 1;
						}
					}
				}//for node j
			}//for node i
		}//close for gen

		fprintf(fp, "%3.4f, ", 100.0*count_block/(float)SIM_NUM_GEN);
		printf("Done\n");

		nsf_free(nsf_net);
	}//close for load

	fprintf(fp, "\n");
	fclose(fp);
	nsf_free(nsfpack);

	printf("\n");
	printf("*************************************************");
	printf(" sucess ");
	printf("*************************************************");
	printf("\n");

	return EXIT_SUCCESS;
} // close main

/*** EOF ***/

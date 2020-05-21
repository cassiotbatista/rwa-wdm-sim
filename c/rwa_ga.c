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

// https://stackoverflow.com/questions/13897835/assign-a-string-created-in-a-function-to-a-typedef-structure-array-created-in-ma
// https://stackoverflow.com/questions/2575048/arrow-operator-usage-in-c
// https://stackoverflow.com/questions/16303677/dynamic-array-of-linked-lists-in-c

#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <stdbool.h>

#include "list.h"
#include "nsf.h"
#include "info.h"
#include "rwa_ga.h"

bool
make_chromosome(nsf* nsf_net, individual* ind, int current_router, int last_router)
{
	int i, j, degree, rnd;
	int *neigh = NULL;

	/* 5. add current node to the path */
	ind->R = list_append(ind->R, current_router);

	/* 6. Repeat steps unless the destination node is found */
	if(current_router == last_router)
		return true;

	degree = 0;
	neigh = malloc(degree * sizeof *neigh);

	/* 2a. get neighbours nodes and current_node degree */
	for(i=0; i<nsf_net->i; i++)
		if(nsf_net->A[current_router][i]) {
			degree++;
			neigh = realloc(neigh, degree * sizeof *neigh);
			neigh[degree-1] = i;
		}

	while(degree) {
		/* 2b. randomly choose one of the nodes */
		rnd = rand() % degree;
		current_router = neigh[rnd];

		/* 2c. pop element from list */
		/* make sure the same node is not chosen twice */
		neigh[rnd] = neigh[--degree]; // move the last element to the popped up position
		neigh = realloc(neigh, degree * sizeof *neigh); // resize list

		/* 3.1 if the chosen node hasn't been visited before */
		if(!list_is_node(ind->R, current_router)) {
			/* 3.2 mark it as the next one in the path */
			/* 5. repeat step 2 by using the next node as the current one */
			if(!make_chromosome(nsf_net, ind, current_router, last_router)) {
				list_remove_rear(ind->R);
				continue;
			} else {
				free(neigh);
				return true;
			}
		} else {
			/* 3.3 otherwise, find another node */
			continue;
		}
	}

	/* release memory allocated for data structures */
	free(neigh);

	/* 4b. if all neighbouring nodes have been visited */
	/* which means current_node has degree 0 or all neighbours are on the path already */
	/* go back one level on the DFS stack by returning FALSE */
	/* which will execute the CONTINUE instruction on line 76. Loop will then run again */
	return false;
}

individual*
_mutate(nsf* nsf_net, individual* chrom_normal)
{
	int start_router, i;
	individual *chrom_trans;
	node* cursor; // r_1, r_2, ..., r_n 
	
	chrom_trans = malloc(sizeof *chrom_trans);
	chrom_trans->R = NULL;


	/* make the mutation point the start router for the subpath */
	start_router = rand() % (chrom_normal->length-1);
	if(start_router == 0 || start_router == chrom_normal->length-1)
		start_router = rand() % (chrom_normal->length-1);

	/* append the source node */
	chrom_trans->R = list_append(chrom_trans->R, chrom_normal->R->data);
	cursor = chrom_normal->R->next; // start right after the source node
	for(i=0; i<start_router; i++) {
		chrom_trans->R = list_append(chrom_trans->R, cursor->data);
		cursor = cursor->next; 
	}

	start_router = cursor->data;

	/* if creation of subpath succeds, return mutated chrom to the population */
	/* discard original chrom, since another one will be returned to the pop */
	if(make_chromosome(nsf_net, chrom_trans, start_router, NSF_DEST_NODE)) {
		chrom_trans->L = calloc(NSF_NUM_CHANNELS, sizeof *(chrom_trans->L));
		return chrom_trans;
	} else {
		/* otherwise, discard mutated chrom and keeps the original on the population */
		list_free(chrom_trans->R);
		free(chrom_trans);
		return chrom_normal;
	}
}

int*
_select(individual **population, int k, int *pop_idxs)
{
	int tourn_times, i, j;
	int *rnd;

	for(j=0; j<2; j++) {
		/* choose a random candidate from population */
		rnd = malloc(2 * sizeof *rnd);
		rnd[0] = rand() % GA_SIZE_POP;

		for(tourn_times=0; tourn_times<k; tourn_times++) {
			/* chose a second random candidate from population */
			rnd[1] = rand() % GA_SIZE_POP;
			while(rnd[0] == rnd[1])
				rnd[1] = rand() % GA_SIZE_POP;

			/* check condition 1: follow the least congested procedure */
			/* choose the route with greater number of available wavelengths */
			if (population[rnd[0]]->chn_free > population[rnd[1]]->chn_free) {
				//population[rnd[1]] = NULL;
			} else if (population[rnd[1]]->chn_free > population[rnd[0]]->chn_free) { 
				rnd[0] = rnd[1];
			} else {
				/* condition 2: follow the first-fit procedure */
				/* choose the route with least weighted, available wavelength */
				for(i=0; i<NSF_NUM_CHANNELS; i++) {
					if(population[rnd[0]]->L[i] ^ population[rnd[1]]->L[i]) {
						if(population[rnd[0]]->L[i]) {
							//candidate->female = NULL;
						} else {
							rnd[0] = rnd[1];
						}
						break;
					}// if different availability is found on L
				}//for first fit

				/* condition 3: follow shortest path procedure */
				/* choose the route with least number of hops */
				if(i == NSF_NUM_CHANNELS) {
					if(population[rnd[0]]->length <= population[rnd[1]]->length) {
						//candidate->female = NULL;
					} else {
						rnd[0] = rnd[1];
					}
				}
			} // else: condition 1 fails
		}//for tourn size k

		pop_idxs[j] = rnd[0];
		free(rnd);
	}//for j

	return pop_idxs;
}

couple*
_cross(individual *father, individual *mother)
{
	int i, n, common_router;
	int *rcommon;  // array of common routers 
	node *mcursor; // cursor for male route R
	node *fcursor; // cursor for female route R

	/* R = [r_1, r_2, r_3, ..., r_(n-2), r(n-1), r_n]
	 * init: start from the node after the source (starts at r_2)
	 * condition: don't let it reach the destination node (stops at r_(n-1))
	 * increment: moves to the next node at each iteration
	 */
	n = 0; // number of common routers
	rcommon = malloc(0 * sizeof *rcommon);
	for(fcursor = mother->R->next; // init
		fcursor->next != NULL;              // condition
		fcursor = fcursor->next)            // increment
		for(mcursor = father->R->next; // init
			mcursor->next != NULL;            // condition
			mcursor = mcursor->next)          // increment
			if(fcursor->data == mcursor->data) {
				n++; // increase the counter of common nodes
				rcommon = realloc(rcommon, n * sizeof *rcommon);
				rcommon[n-1] = fcursor->data;
			}

	/* if there's no common router, do not perform crossover */
	if(n == 0) {
		free(rcommon);
		return NULL;
	}
	
	/* pick a random router among all the common routers */
	common_router = rcommon[rand() % n];
	free(rcommon);

	/* allocate memory for offspring */
	couple* offspring;
	offspring = malloc(sizeof *offspring);

	/* allocate memory for the children */
	offspring->male = malloc(sizeof *(offspring->male));
	offspring->female = malloc(sizeof *(offspring->female));

	offspring->male->R = NULL;
	offspring->female->R = NULL;

	/* fill first half of son: it comes from the father */
	mcursor = father->R;
	while(mcursor->data != common_router) {
		offspring->male->R = list_append(offspring->male->R, mcursor->data);
		mcursor = mcursor->next;
	}

	/* fill first half of daughter: it comes from the mother */
	fcursor = mother->R;
	while(fcursor->data != common_router) {
		offspring->female->R = list_append(offspring->female->R, fcursor->data);
		fcursor = fcursor->next;
	}

	/* fill second half of son: it comes from the mother */
	while(fcursor != NULL) {
		offspring->male->R = list_append(offspring->male->R, fcursor->data);
		fcursor = fcursor->next;
	}

	/* fill second half of daughter: it comes from the father */
	while(mcursor != NULL) {
		offspring->female->R = list_append(offspring->female->R, mcursor->data);
		mcursor = mcursor->next;
	}

	/* fill son's metadata */
	offspring->male->L = calloc(NSF_NUM_CHANNELS, sizeof *(offspring->male->L));
	offspring->male->chn_free = 0;
	offspring->male->length = list_count(offspring->male->R);

	/* fill daughter's metadata */
	offspring->female->L = calloc(NSF_NUM_CHANNELS, sizeof *(offspring->female->L));
	offspring->female->chn_free = 0;
	offspring->female->length = list_count(offspring->female->R);

	return offspring;
}

individual*
evaluate(individual* ind, nsf* N)
{
	int i, l, w;
	int rcurr, rnext;
	int num;

	node* rcursor;

	/* number of links */
	ind->length = list_count(ind->R);
	l = ind->length-1;

	/* reset number of free channels */
	ind->chn_free = 0;

	/* iterate at the weight w of each wavelength */
	for(w=1; w<=N->w; w++) {
		num = 0;
		rcursor = ind->R;
		for(i=0; i<l; i++) {
			rcurr = rcursor->data;
			rnext = rcursor->next->data;

			/* TODO: cast bool2int? */
			/* calculate GOF's numerator parameter */
			//printf("(%d) NSF[%d][%d][%d]\n", N->w, rcurr, rnext, w-1);
			num += w * N->N[rcurr][rnext][w-1];

			rcursor = rcursor->next;
		}// close for l

		/* store full boolean GOF label L for wavelength of weight w */
		ind->L[w-1] = (int)(num/(float)(w*l));

		/* update number of channels free */
		ind->chn_free += (int)ind->L[w-1];
	}// close for w

	return ind;
}

void 
insertion_sort(individual **pop, int size)
{
	int i, j, k;
	int ii;
	individual *ind;

	for(j=1; j<size; j++) {
		ind = pop[j];
		i = j-1;

		while(i >= 0) {
			if(pop[i]->chn_free < ind->chn_free) {
				/* condition 1: order by number of free channels */
				pop[i+1] = pop[i--];
			} else if(pop[i]->chn_free == ind->chn_free) {
				/* condition 2: order by first wavelength available */
				for(ii=0; ii<NSF_NUM_CHANNELS; ii++) {
					if(pop[i]->L[ii] ^ ind->L[ii]) {
						if(!pop[i]->L[ii]) {
							pop[i+1] = pop[i--];
						} else {
							ii = NSF_NUM_CHANNELS+1; // A[i] < key .:. pop[i]->L > ind->L
						}
						break; // break for loop
					}//close if XOR
				}//close for ii

				if(ii == NSF_NUM_CHANNELS) {
					/* condition 3: order by least number of hops */
					if(pop[i]->length <= ind->length)
						pop[i+1] = pop[i--];
					else
						break; // A[i] < key .:. pop[i]->length > ind->length 
				} else if(ii > NSF_NUM_CHANNELS) {
					break;
				}
			} else {
				break; // A[i] < key .:. pop[i]->chn_free < ind->chn_free
			}
		}//close while i

		pop[i+1] = ind;
	}//close for j
} //close sort

void
individual_free(individual *ind)
{
	list_free(ind->R);
	free(ind->L);
	free(ind);
}

int
rwa(nsf **G, float holding_time)
{
	int i, j, w;
	individual** population;
	int* parents;
	couple* offspring;
	node* cursor;
	int rcurr, rnext;
	int color;

	int generation;
	float Pc = GA_MAX_CROSS_RATE;
	float Pm = GA_MIN_MUT_RATE;
	int k = 3;

	parents = malloc(2 * sizeof *parents);

	/* init population */
	/* allocate memory for the population data structure */
	population = malloc(GA_SIZE_POP * sizeof *population); 

	/* build chromosomes */
	for(i=0; i<GA_SIZE_POP; i++) {
		population[i] = malloc(sizeof *(population[i]));
		population[i]->R = NULL;
		population[i]->L = NULL;

		if(make_chromosome(G, population[i], NSF_SOURCE_NODE, NSF_DEST_NODE)) {
			population[i]->L = calloc(NSF_NUM_CHANNELS, sizeof *(population[i]->L));
			population[i]->chn_free = 0;
			population[i]->length = list_count(population[i]->R);
		} else {
			list_free(population[i]->R); 
			free(population[i]);
			i--;
		}
	}// for i = size_pop

	/* ****************************************************************** */
	/* ################### Genetic algorithm main loop ################## */
	/* ------------------------------------------------------------------ */
	for(generation=0; generation<GA_MIN_GEN; generation++) {
		/* evaluate each and every individual of the population */
		for(i=0; i<GA_SIZE_POP; i++)
			population[i] = evaluate(population[i], G);

		/* rearrange (sort by fitness) */
		insertion_sort(population, GA_SIZE_POP);

		int last_chrom = GA_SIZE_POP-1;
		for(i=0; i<GA_SIZE_POP; i++) {
			parents = _select(population, k, parents);

			if(Pc > rand()/(float)RAND_MAX) {
				/* select individuals to reproduce via tournament approach */
				/* choose a couple to put on the mating pool */
				/* reproduce individuals via one-point crossover */

				/* cross */
				offspring = _cross(population[parents[0]], population[parents[1]]);

				if(offspring != NULL) {
					for(j=0; j<2; j++) {
						// remove the last chromossome...
						list_free(population[last_chrom]->R);
						free(population[last_chrom]->L);
						free(population[last_chrom]);

						// ... and replace it by the one of the children
						// Tip: struct metadata is filled by cross()
						if(j == 0)
							population[last_chrom] = offspring->male;
						else 
							population[last_chrom] = offspring->female;

						last_chrom--; // update the last
					}
				}//if offspring

				i++; // skip check for one ind since two are picked at a time
			}

			if(Pm > rand()/(float)RAND_MAX) {
				population[parents[0]] = _mutate(G, population[parents[0]]);
			}

			for(i=0; i<GA_SIZE_POP; i++)
				population[i] = evaluate(population[i], G);
			} // for each individual (i)
	}//for generation

	free(parents);

	// evaluate for the last time
	for(i=0; i<GA_SIZE_POP; i++)
		population[i] = evaluate(population[i], G);

	/* rearrange (sort by fitness) */
	insertion_sort(population, GA_SIZE_POP);

	if(population[0]->chn_free > 0) {
		for(i=0; i<NSF_NUM_CHANNELS; i++)
			if((color = population[0]->L[i]) == 1)
				break;
	
		for(cursor=population[0]->R; cursor->next!=NULL; cursor=cursor->next) {
			rcurr = cursor->data;
			rnext = cursor->next->data;

			*(G->N[rcurr][rnext][color]) = *(G->N[rnext][rcurr][color]) = 0;
			*(G->T[rcurr][rnext][color]) = *(G->T[rnext][rcurr][color]) = holding_time;
		}

		/* free memory allocated for each individual */
		for(i=0; i<GA_SIZE_POP; i++) 
			individual_free(population[i]);
		free(population);

		return 0; // allocated 
	} else {
		/* free memory allocated for each individual */
		for(i=0; i<GA_SIZE_POP; i++)
			individual_free(population[i]);
		free(population);

		return 1; // blocked
	}

}//close rwa

/*** EOF ***/

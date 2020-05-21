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
	int* neigh = NULL;

	/* 5. add current node to the path */
	list_append(ind->R, current_router);

	/* 6. Repeat steps unless the destination node is found */
	if(current_router == last_router)
		return true;

	degree = 0;
	neigh = (int*)malloc(degree * sizeof(int));

	/* 2a. get neighbours nodes and current_node degree */
	for(i=0; i<nsf_net->i; i++)
		if(nsf_net->A[current_router][i]) {
			degree++;
			neigh = (int*)realloc(neigh, degree*sizeof(*neigh));
			neigh[degree-1] = i;
		}

	while(degree) {
		/* 2b. randomly choose one of the nodes */
		rnd = rand() % degree;
		current_router = neigh[rnd];
		
		/* 2c. pop element from list */
		/* make sure the same node is not chosen twice */
		neigh[rnd] = neigh[--degree]; // move the last element to the popped up position
		neigh = (int*)realloc(neigh, degree*sizeof(*neigh)); // resize list

		/* 3.1 if the chosen node hasn't been visited before */
		if(list_search(ind->R, current_router) != NULL) {
			/* 3.2 mark it as the next one in the path */
			/* 5. repeat step 2 by using the next node as the current one */
			if(!make_chromosome(nsf_net, ind, current_router, last_router)) {
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
	free(ind->R); 

	/* 4b. if all neighbouring nodes have been visited */
	/* which means current_node has degree 0 or all neighbours are on the path already */
	/* go back one level on the DFS stack by returning FALSE */
	/* which will execute the CONTINUE instruction on line 76. Loop will then run again */
	return false;
}

individual*
mutate(nsf* nsf_net, individual* chrom_normal, float Pm)
{
	int start_router;
	individual* chrom_trans;
	node* cursor; // r_1, r_2, ..., r_n 

	chrom_trans = (individual*)malloc(sizeof(individual));
	chrom_trans->R = (node*)malloc(sizeof(node));
	cursor = (node*)malloc(sizeof(node));

	/* check probability of mutation for each gene */
	//cursor = list_deep_copy(chrom_normal->R, cursor);
	for(cursor = chrom_normal->R;
		cursor->next != NULL;
		cursor = cursor->next) 
	{
		if(Pm > rand()/(float)RAND_MAX)
			break;
		else
			chrom_trans->R = list_append(chrom_trans->R, cursor->data);
	}

	/* make the mutation point the start router for the subpath */
	start_router = cursor->data;
	//list_free(cursor);

	/* if mutation point is the destination router, do not perform mutation */
	if(start_router == NSF_DEST_NODE) {
		list_free(chrom_trans->R);
		free(chrom_trans);
		return chrom_normal;
	}

	/* if creation of subpath succeds, return mutated chrom to the population */
	/* discard original chrom, since another one will be returned to the pop */
	if(make_chromosome(nsf_net, chrom_trans, start_router, NSF_DEST_NODE)) {
		list_free(chrom_normal->R);
		chrom_normal->R = (node*)malloc(sizeof(node));
		return chrom_trans;
	} else {
		/* otherwise, discard mutated chrom and keeps the original on the population */
		list_free(chrom_trans->R);
		return chrom_normal;
	}
}

couple*
_select(individual** population, int k)
{
	int tourn_times, i, j;
	couple* parents;
	couple* candidate;

	candidate = (couple*)malloc(sizeof(couple));
	//parents = (couple*)malloc(sizeof(couple));

	for(j=0; i<2; j++) {
		/* choose a random candidate from population */
		candidate->male = population[rand() % GA_SIZE_POP];

		for(tourn_times=0; tourn_times<k; tourn_times++) {
			/* chose a second random candidate from population */
			candidate->female = population[rand() % GA_SIZE_POP];

			/* check condition 1: follow the least congested procedure */
			/* choose the route with greater number of available wavelengths */
			if (candidate->male->chn_free > candidate->female->chn_free) {
				candidate->female = NULL;
			} else if (candidate->female->chn_free > candidate->male->chn_free) { 
				candidate->male = candidate->female;
				candidate->female = NULL;
			} else { 
				/* condition 2: follow the first-fit procedure */
				/* choose the route with least weighted, available wavelength */
				for(i=0; i<NSF_NUM_CHANNELS; i++) {
					if(candidate->male->L[i] ^ candidate->female->L[i]) {
						if(candidate->male->L[i]) {
							candidate->female = NULL;
							break;
						} else {
							candidate->male = candidate->female;
							candidate->female = NULL;
							break;
						}
					}// if different availability is found on L
				}//for first fit

				/* condition 3: follow shortest path procedure */
				/* choose the route with least number of hops */
				if(i == NSF_NUM_CHANNELS) {
					if(candidate->male->length >= candidate->female->length) {
						candidate->female = NULL;
					} else {
						candidate->male = candidate->female;
						candidate->female = NULL;
					}
				}
			} // else: condition 1 fails
		}//for tourn size k

		if(j == 0)
			parents->male = candidate->male;
		else
			parents->female = candidate->female;
	}//for j

	return parents;
}

couple*
cross(couple* parents)
{
	int i, n, common_router;
	int* rcommon;  // array of common routers 
	node* mcursor; // cursor for male route R
	node* fcursor; // cursor for female route R

	couple* offspring;

	/* R = [r_1, r_2, r_3, ..., r_(n-2), r(n-1), r_n]
	 * init: start from the node after the source (starts at r_2)
	 * condition: don't let it reach the destination node (stops at r_(n-1))
	 * increment: moves to the next node at each iteration
	 */
	n = 0; // number of common routers
	rcommon = (int*)malloc(0*sizeof(int));
	for(fcursor = parents->female->R->next; // init
		fcursor->next != NULL;              // condition
		fcursor = fcursor->next)            // increment
		for(mcursor = parents->male->R->next; // init
			mcursor->next != NULL;            // condition
			mcursor = mcursor->next)          // increment
			if(fcursor->data == mcursor->data) {
				n++; // increase the counter of common nodes
				rcommon = (int*)realloc(rcommon, n*sizeof(*rcommon));
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
	offspring = (couple*)malloc(sizeof(couple));

	/* allocate memory for the son */
	offspring->male = (individual*)malloc(sizeof(individual));
	offspring->male->R = NULL;

	/* fill son */
	/* fill first half of son: it comes from the father */
	for(mcursor = parents->male->R; // starts at the head of father's R
		mcursor->data == common_router; // stops when the common router is reached
		mcursor = mcursor->next // moves to the next node at each iteration
	)
		offspring->male->R = list_append(offspring->male->R, mcursor->data);

	/* fill second half of son: it comes from the mother */
	for(fcursor = list_search(parents->female->R, common_router); // start: mom's rcommon 
		fcursor != NULL; // stops at the last node, i.e., destination node
		fcursor = fcursor->next // moves to the next node at each iteration
	)
		offspring->male->R = list_append(offspring->male->R, fcursor->data);

	/* fill son's metadata */
	offspring->male->L = (bool*)calloc(NSF_NUM_CHANNELS, sizeof(bool));
	offspring->male->chn_free = 0;
	offspring->male->length = list_count(offspring->male->R);

	/* allocate memory for the daughter */
	offspring->female = (individual*)malloc(sizeof(individual));
	offspring->female->R = NULL;

	/* fill daughter */
	/* fill first half of daughter: it comes from the mother */
	for(fcursor = parents->female->R; // starts at the head of mother's R
		fcursor->data == common_router; // stops when the common router is reached
		fcursor = fcursor->next // moves to the next node at each interation
	)
		offspring->female->R = list_append(offspring->female->R, fcursor->data);

	/* fill second half of daughter: it comes from the father */
	for(mcursor = list_search(parents->male->R, common_router); // start: dad's rcommon
		mcursor != NULL; // stops at the last node, i.e., destination node
		mcursor = mcursor->next // moves to the next node at each iteration
	)
		offspring->female->R = list_append(offspring->female->R, mcursor->data);

	/* fill daughter's metadata */
	offspring->female->L = (bool*)calloc(NSF_NUM_CHANNELS, sizeof(bool));
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

	node* rcursor = ind->R;

	/* number of links */
	ind->length = list_count(ind->R);
	l = ind->length-1;

	/* iterate at the weight w of each wavelength */
	for(w=1; w<=N->w; w++) {
		num = 0;
		for(i=0; i<l; i++) {
			rcurr = rcursor->data;
			rnext = rcursor->next->data;

			/* TODO: cast bool2int? */
			/* calculate GOF's numerator parameter */
			num += w * N->N[rcurr][rnext][w-1];

			rcursor = rcursor->next;
		}// close for l

		/* update number of channels free */
		ind->chn_free += (int)(num/(float)(w*l));

		/* store full boolean GOF label L for wavelength of weight w */
		ind->L[w-1] = (bool)ind->chn_free;
	}// close for w

	return ind;
}

void 
insertion_sort(individual **pop, int size)
{
	int i, j;
	int ii;
	individual* ind;

	for(j=1; j<size; j++) {
		ind = pop[j];
		i = j-1;

		while(i >= 0) {
			if(pop[i]->chn_free > ind->chn_free) {
				/* condition 1: order by number of free channels */
				pop[i+1] = pop[i--];
			} else if(pop[i]->chn_free == ind->chn_free) {
				/* condition 2: order by first wavelength available */
				for(ii=0; ii<NSF_NUM_CHANNELS; ii++) 
					if(pop[i]->L[ii] ^ ind->L[ii]) {
						if(pop[i]->L[ii]) {
							pop[i+1] = pop[i--];
						} else {
							i = -1; // A[i] < key .:. pop[i]->L > ind->L
							break;
						}
					}

				if(ii == NSF_NUM_CHANNELS) {
					/* condition 3: order by least number of hops */
					if(pop[i]->length >= ind->length)
						pop[i+1] = pop[i--];
					else
						break; // A[i] < key .:. pop[i]->length > ind->length 
				}
			} else {
				break; // A[i] < key .:. pop[i]->chn_free < ind->chn_free
			}
		}//close while i

		pop[i+1] = ind;
	}//close for j
} //close sort

int
rwa(nsf *G, float holding_time)
{
	int i, j, w;
	individual** population;
	couple* parents;
	couple* offspring;
	node* cursor;
	int rcurr, rnext;
	int color;

	int generation;
	float Pc = GA_MAX_CROSS_RATE;
	float Pm = GA_MIN_MUT_RATE;
	int k = 3;
	

	/* init population */
	/* allocate memory for the population data structure */
	population = (individual**)malloc(GA_SIZE_POP * sizeof(individual*)); 

	/* build chromosomes */
	for(i=0; i<GA_SIZE_POP; i++) {
		population[i] = (individual*)malloc(sizeof(individual));
		population[i]->R = NULL;
		population[i]->L = NULL;

		if(make_chromosome(G, population[i], NSF_SOURCE_NODE, NSF_DEST_NODE)) {
			population[i]->L = (bool*)calloc(NSF_NUM_CHANNELS, sizeof(bool));
			population[i]->chn_free = 0;
			population[i]->length = list_count(population[i]->R);
		} else {
			// Tip: make_chromosome already frees R
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
			if(Pc > rand()/(float)RAND_MAX) {
				/* select individuals to reproduce via tournament approach */
				/* choose a couple to put on the mating pool */
				parents = _select(population, k);

				/* mutate the entire mating pool */
				/* x-man is in-place transformed */
				parents->male = mutate(G, parents->male, Pm);
				parents->female = mutate(G, parents->female, Pm);

				/* reproduce individuals via one-point crossover */
				/* cross */
				offspring = cross(parents);
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
		} // for each individual (i)
	}//for generation

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

			G->N[rcurr][rnext][color] = G->N[rnext][rcurr][color] = 0;
			G->T[rcurr][rnext][color] = G->T[rnext][rcurr][color] = holding_time;
		}
		return 0; // allocated 
	} else {
		return 1; // blocked
	}

}//close rwa

/*** EOF ***/

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

#ifndef LIST_H_
#define LIST_H_
 
#include <stdbool.h>

//typedef struct node node;
typedef struct node {
	int data;
	struct node* next;
} node;

node* list_create_node(node* next, int data);
void  list_print(node *head);
int   list_count(node* head);
node* list_prepend(node* head, int data);
node* list_append(node* head, int data);
node* list_insert_after(node* head, node* prev, int data);
node* list_insert_before(node* head, node* next, int data);
bool  list_is_node(node* head, int key);
node* list_search(node* head, int key);
node* list_remove_front(node* head);
node* list_remove_rear(node* head);
node* list_remove_any(node* head, node* nd);
void  list_free(node *head);

#endif
/*** EOF ***/

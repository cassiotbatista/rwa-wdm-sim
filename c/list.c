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

// http://www.zentut.com/c-tutorial/c-linked-list/

#include <stdio.h>
#include <stdlib.h>
#include <stdbool.h>

#include "list.h"

node*
list_create_node(node* next, int data) 
{
	node *new_node = malloc(sizeof *new_node);
	if(new_node == NULL) {
		fprintf(stderr, "error\n");
		exit(0);
	}

	new_node->data = data;
	new_node->next = next;

	return new_node;
}

void
list_print(node *head)
{
	node *cursor = head;
	while(cursor != NULL) {
		printf("%d ", cursor->data);
		cursor = cursor->next;
	}
	printf("\n");
}

int
list_count(node *head)
{
	if(head == NULL)
		fprintf(stderr, "EITA\n");

	node *cursor = head;
	int c = 0;
	while(cursor != NULL) {
		c++;
		cursor = cursor->next;
	}
	return c;
}

node*
list_prepend(node* head, int data)
{
	node* new_node = list_create_node(head, data);
	head = new_node;
	return head;
}

node*
list_append(node* head, int data)
{
	if(head == NULL)
		return list_prepend(head, data);

	node *cursor = head;
	while(cursor->next != NULL)
		cursor = cursor->next;

	node* new_node = list_create_node(NULL, data);
	cursor->next = new_node;

	return head;
}

node*
list_insert_after(node* head, node* prev, int data)
{
	node* cursor = head;
	while(cursor != prev)
		cursor = cursor->next;

	if(cursor != NULL) {
		node *new_node = list_create_node(cursor->next, data);
		cursor->next = new_node;
		return head;
	} else {
		return NULL;
	}
}

node*
list_insert_before(node* head, node* next, int data)
{
	if(next == NULL || head == NULL) {
		return NULL;
	} else if(head == next) {
		head = list_prepend(head, data);
		return head;
	}

	node* cursor = head;
	while(cursor != NULL) {
		if(cursor->next == next)
			break;
		cursor = cursor->next;
	}

	if(cursor != NULL) {
		node *new_node = list_create_node(cursor->next, data);
		cursor->next = new_node;
		return head;
	} else {
		return NULL;
	}
}

bool
list_is_node(node* head, int key)
{
	if(head == NULL)
		fprintf(stderr, "HEAD NULL\n");

	node* cursor = head;
	while(cursor != NULL) {
		if(cursor->data == key)
			return true;
		cursor = cursor->next;
	}

	return false;
}

node*
list_search(node* head, int key)
{
	node *cursor = head;
	while(cursor != NULL) {
		if(cursor->data == key)
			return cursor;
		cursor = cursor->next;
	}

	return NULL;
}

node*
list_remove_front(node* head)
{
	if(head == NULL)
		return NULL;

	node *front = head;
	head = head->next;
	front->next = NULL;

	/* is this the last node in the list */
	if(front == head)
		head = NULL;

	free(front);
	return head;
}

node*
list_remove_rear(node* head)
{
	if(head == NULL)
		return NULL;

	node* cursor = head;
	node* back = NULL;
	while(cursor->next != NULL) {
		back = cursor;
		cursor = cursor->next;
	}

	if(back != NULL)
		back->next = NULL;

	if(cursor == head)
		head = NULL;

	free(cursor);
	return head;
}

node*
list_remove_any(node* head, node* nd)
{
	/* if the node is the first node */
	if(nd == head) {
		head = list_remove_front(head);
		return head;
	}

	/* if the node is the last node */
	if(nd->next == NULL) {
		head = list_remove_rear(head);
		return head;
	}

	/* if the node is in the middle */
	node* cursor = head;
	while(cursor != NULL) {
		if(cursor->next = nd)
			break;
		cursor = cursor->next;
	}

	if(cursor != NULL) {
		node* tmp = cursor->next;
		cursor->next = tmp->next;
		tmp->next = NULL;
		free(tmp);
	}
	return head;
}

void
list_free(node *head)
{
	node *cursor, *tmp;

	if(head == NULL)
		return;

	cursor = head->next;
	head->next = NULL;

	while(cursor != NULL) {
		tmp = cursor->next;
		free(cursor);
		cursor = tmp;
	}

	free(head);
}

node*
list_deep_copy(node* head, node* copy)
{
	if(head == NULL || copy == NULL) {
		fprintf(stderr, "No memory has been allocated to lists yet.\n");
		return NULL;
	}

	node* cursor;
	for(cursor=head; cursor!=NULL; cursor=cursor->next) 
		copy = list_append(copy, cursor->data);

	return copy;
}

/*** EOF ***/

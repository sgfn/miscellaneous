#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>

#define BUFFER_SIZE 1024
#define MEMORY_ALLOCATION_ERROR  -1
#define LIST_ERROR               -2
#define PROGRAM_ERROR            -3

#define DELIMS " \r\t\n.,?!:;-"

struct tagList;
typedef void (*ConstDataFp)(const void*);
typedef void (*DataFp)(void*);
typedef  int (*CompareDataFp)(const void*, const void*);
typedef void (*InsertInOrder)(struct tagList*, void*);

typedef struct tagListElement {
	struct tagListElement *next;
	void                  *data;
} ListElement;

typedef struct tagList {
	ListElement *head;
	ListElement *tail;
	ConstDataFp dump_data;
	DataFp      free_data;
	CompareDataFp compare_data;
	InsertInOrder insert_sorted;
} List;

// -----------------------------------------------------------------
// generic functions - they are common for all instances of the list
// (independent of the data type)
// -----------------------------------------------------------------

void init_list(List *p_list, ConstDataFp dump_data, DataFp free_data,
			   CompareDataFp compare_data, InsertInOrder insert_sorted) {
	p_list->head = NULL;
	p_list->tail = NULL;
	p_list->dump_data = dump_data;
	p_list->free_data = free_data;
	p_list->compare_data = compare_data;
	p_list->insert_sorted = insert_sorted;
}

// Print all elements of the list
void dump_list(const List* p_list) {
	ListElement *element = p_list->head;
	while(element) {
		p_list->dump_data(element->data);
		element = element->next;
	}
	printf("\n");
}

// Print elements of the list if comparable to data
void dump_list_if(List *p_list, void *data) {
	ListElement *element = p_list->head;
	while(element) {
		if(p_list->compare_data(element->data, data) == 0) p_list->dump_data(element->data);
		element = element->next;
	}
}

// Free all elements of the list
void free_list(List* p_list) {
	ListElement *element = p_list->head, *next_element;
	while(element) {
		next_element = element->next;
		p_list->free_data(element->data);
		free(element);
		element = next_element;
	}
	p_list->head = NULL;
	p_list->tail = NULL;
}

// Push element at the beginning of the list
void push_front(List *p_list, void *data) {
	ListElement *element = malloc(sizeof(ListElement));
	if(element == NULL) exit(MEMORY_ALLOCATION_ERROR);
	element->data = data;
	element->next = p_list->head;

	p_list->head = element;
	if(!p_list->tail) p_list->tail = p_list->head;
}

// Push element at the end of the list
void push_back(List *p_list, void *data) {
	ListElement *element = malloc(sizeof(ListElement));
	if(element == NULL) exit(MEMORY_ALLOCATION_ERROR);
	element->data = data;
	element->next = NULL;

	if(p_list->tail) p_list->tail->next = element;
	p_list->tail = element;
	if(!p_list->head) p_list->head = p_list->tail;
}

// Remove the first element
void pop_front(List *p_list) {
	if(!p_list->head) return;
	ListElement *element = p_list->head;
	p_list->head = p_list->head->next;

	p_list->free_data(element->data);
	free(element);
	if(!p_list->head) p_list->tail = NULL;
}

// Reverse the list
void reverse(List *p_list) {
	if(!p_list->head) return;
	ListElement *element_prev = NULL, *element_curr = p_list->head, *element_next;
	while(element_curr) {
		element_next = element_curr->next;
		element_curr->next = element_prev;
		element_prev = element_curr;
		element_curr = element_next;
	}
	element_next = p_list->head;
	p_list->head = p_list->tail;
	p_list->tail = element_next;
}

// insert element preserving the ordering (defined by insert_sorted function)
void insert_in_order(List *p_list, void *data) {
	p_list->insert_sorted(p_list, data);
}

// find element in sorted list after which to insert given element
ListElement* find_insertion_point(const List *p_list, ListElement *p_element) {
	ListElement *element_curr = p_list->head, *element_prev = NULL;
	while(element_curr) {
		if(p_list->compare_data(element_curr->data, p_element->data) > 0) break;
		element_prev = element_curr;
		element_curr = element_curr->next;
	}
	return element_prev;
}

// Insert element after 'previous'
void push_after(List *p_list, void *data, ListElement *previous) {
	ListElement *element = malloc(sizeof(ListElement));
	element->data = data;

	if(!previous) {
		element->next = p_list->head;
		p_list->head = element;
	}
	else {
		element->next = previous->next;
		previous->next = element;
	}
	if(!p_list->tail) p_list->tail = p_list->head;
	if(!element->next) p_list->tail = element;
}

// Insert element preserving order (no counter)
void insert_elem(List *p_list, void *p_data) {
	ListElement temp_element;
	temp_element.data = p_data;
	temp_element.next = NULL;
	ListElement *previous = find_insertion_point(p_list, &temp_element);

	if (!previous || p_list->compare_data(previous->data, p_data) != 0)
		push_after(p_list, p_data, previous);
}

// ---------------------------------------------------------------
// type-specific definitions
// ---------------------------------------------------------------

// int element

typedef struct DataInt {
	int id;
} DataInt;

void dump_int(const void *d) {
	printf("%d ", ((DataInt*)d)->id);
}

void free_int(void *d) {
	free((DataInt*)d);
}

int cmp_int(const void *a, const void *b) {
	return ((DataInt*)a)->id - ((DataInt*)b)->id;
}

DataInt *create_data_int(int v) {
	DataInt *dint = malloc(sizeof(DataInt));
	dint->id = v;
	return dint;
}

// Word element

typedef struct DataWord {
	char *word;
	int counter;
} DataWord;

void dump_word (const void *d) {
	printf("%s\n", ((DataWord*)d)->word);
}

void dump_word_lowercase (const void *d) {
	dump_word(d);
	// printf("%s %d\n", ((DataWord*)d)->word, ((DataWord*)d)->counter);
}

void free_word(void *d) {
	free(((DataWord*)d)->word);
	free((DataWord*)d);
}

// conpare words case insensitive
int cmp_word_alphabet(const void *a, const void *b) {
	return strcmp( ((DataWord*)a)->word, ((DataWord*)b)->word );
}

int cmp_word_counter(const void *a, const void *b) {
	return ((DataWord*)a)->counter - ((DataWord*)b)->counter;
}

DataWord *create_data_word(char *str, int lower) {
	DataWord *dwrd = malloc(sizeof(DataWord));
	dwrd->word = malloc(strlen(str)+1);
	if (lower == 1) {
		for (int i=0; str[i]; ++i)	str[i] = tolower(str[i]);
	}
	strcpy(dwrd->word, str);

	dwrd->counter = 1;
	return dwrd;
}


// insert element; if present increase counter
void insert_elem_counter(List *p_list, void *data) {
	ListElement temp_element;
	temp_element.data = data;
	temp_element.next = NULL;
	ListElement* previous = find_insertion_point(p_list, &temp_element);
	if(previous && p_list->compare_data(previous->data, data) == 0)
			((DataWord*)(previous->data))->counter++;
	else	push_after(p_list, data, previous);
}

// read text, parse it to words, and insert those words to the list
// in order given by the last parameter (0 - read order,
// 1 - alphabetical order)
void stream_to_list(List *p_list, FILE *stream, int order) {
	char buffer[BUFFER_SIZE], c;
	while ((c = getc(stream)) != EOF) {
		ungetc(c, stream);
		fgets(buffer, BUFFER_SIZE, stream);
		char* t = strtok(buffer, DELIMS);
		while (t != NULL) {
			if (order == 0) push_back(p_list, create_data_word(t, order));
			else 			p_list->insert_sorted(p_list, create_data_word(t, order));
			t = strtok(NULL, DELIMS);
		}
	}
}

// test integer list
void list_test(List *p_list, int n) {
	char op[2];
	int v;
	for (int i = 0; i < n; ++i) {
		// dump_list(p_list);
		scanf("%s", op);
		switch (op[0]) {
			case 'f':
				scanf("%d", &v);
				push_front(p_list, create_data_int(v));
				break;
			case 'b':
				scanf("%d", &v);
				push_back(p_list, create_data_int(v));
				break;
			case 'd':
				pop_front(p_list);
				break;
			case 'r':
				reverse(p_list);
				break;
			case 'i':
				scanf("%d", &v);
				insert_in_order(p_list, create_data_int(v));
				break;
			default:
				printf("No such operation: %s\n", op);
				break;
		}
	}
}

int main(void) {
	int to_do, n;
	List list;

	scanf ("%d", &to_do);
	switch (to_do) {
		case 1: // test integer list
			scanf("%d",&n);
			init_list(&list, dump_int, free_int,
					  cmp_int, insert_elem);
			list_test(&list, n);
			dump_list(&list);
			free_list(&list);
			break;
		case 2: // read words from text, insert into list, and print
			init_list(&list, dump_word, free_word,
					  cmp_word_alphabet, insert_elem_counter);
			stream_to_list(&list, stdin, 0);
			dump_list(&list);
			free_list(&list);
			break;
		case 3: // read words, insert into list alphabetically, print words encountered n times
			scanf("%d",&n);
			init_list(&list, dump_word_lowercase, free_word,
			          cmp_word_alphabet, insert_elem_counter);
			stream_to_list(&list, stdin, 1);
			list.compare_data = cmp_word_counter;
			DataWord data = { NULL, n };
//			list.dump_data = dump_word_lowercase;
			dump_list_if(&list, &data);
			printf("\n");
			free_list(&list);
			break;
		default:
			printf("NOTHING TO DO FOR %d\n", to_do);
			break;
	}
	return 0;
}


#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#include <math.h>

#define BUFFER_SIZE 1024
#define MAX_RATE 4
#define MEMORY_ALLOCATION_ERROR  -1
#define LIST_ERROR               -2
#define PROGRAM_ERROR            -3

#define DELIMS " \r\t\n.,?!:;-"

typedef union data_union {
	int int_data;
	char char_data;
	void *ptr_data;
} data_union;

typedef void (*DataFp)(data_union);
typedef void (*DataPFp)(data_union*);
typedef  int (*CompareDataFp)(data_union, data_union);
typedef  int (*HashFp)(data_union, int);

typedef struct ht_element {
	struct ht_element *next;
	data_union data;
} ht_element;

typedef struct hash_table {
	int size;
	int no_elements;
	ht_element **ht;
	DataFp dump_data;
	DataFp free_data;
	CompareDataFp compare_data;
	HashFp hash_function;
	DataPFp modify_data;
} hash_table;

void *safe_malloc(size_t size) {
	void *ptr = malloc(size);
	if(ptr) return ptr;
	exit(MEMORY_ALLOCATION_ERROR);
}

// ---------------------- functions to implement

// initialize table fields
void init_ht(hash_table *p_table, int size, DataFp dump_data, DataFp free_data,
		 CompareDataFp compare_data, HashFp hash_function, DataPFp modify_data) {
	p_table->size = size;
	p_table->no_elements = 0;
	p_table->ht = safe_malloc(size * sizeof(ht_element*));
	memset(p_table->ht, 0, size * sizeof(ht_element*));

	p_table->dump_data = dump_data;
	p_table->free_data = free_data;
	p_table->compare_data = compare_data;
	p_table->hash_function = hash_function;
	p_table->modify_data = modify_data;
}

// print elements of the list with hash n
void dump_list(const hash_table* p_table, int n) {
	ht_element *p = p_table->ht[n];
	while(p) {
		p_table->dump_data(p->data);
		p = p->next;
	}
	printf("\n");
}

// Free element pointed by data_union using free_data() function
void free_element(DataFp free_data, ht_element *to_delete) {
	if(free_data)	free_data(to_delete->data);
	free(to_delete);
}

// free all elements from the table (and the table itself)
void free_table(hash_table* p_table) {
	ht_element *p, *q;
	for(int i=0; i<p_table->size; ++i) {
		p = p_table->ht[i];
		while(p) {
			q = p->next;
			// printf("FREEING %d \n", p->data.int_data);
			free_element(p_table->free_data, p);
			p = q;
		}
	}
	free(p_table->ht);
}

// calculate hash function for integer k
int hash_base(int k, int size) {
	static const double c = 0.618033988; // (sqrt(5.) – 1) / 2.;
	double tmp = k * c;
	return (int)floor(size * (tmp - floor(tmp)));
}

void rehash(hash_table *p_table) {
	// create a temporary linked list of all elements
	ht_element sentinel, *prev = &sentinel, *p, *q;
	sentinel.next = NULL;
	for(int i=0; i<p_table->size; ++i) {
		p = p_table->ht[i];
		while(p) {
			prev->next = p;
			prev = p;
			p = p->next;
		}
	}
	// resize the table of pointers and set them to NULL
	p_table->size *= 2;
	p_table->ht = realloc(p_table->ht, p_table->size * sizeof(ht_element*));
	// for(ht_element **p=p_table->ht; p; ++p) *p = NULL;
	memset(p_table->ht, 0, p_table->size * sizeof(ht_element*));
	// calculate new hashes and insert elements in appropriate spots
	p = sentinel.next;
	while(p) {
		int i = p_table->hash_function(p->data, p_table->size);
		q = p->next;
		p->next = p_table->ht[i];
		p_table->ht[i] = p;
		p = q;
	}
}

// find element; return pointer to previous
ht_element *find_previous(hash_table *p_table, data_union data, int *first) {
	int i = p_table->hash_function(data, p_table->size);
	ht_element *p = p_table->ht[i], *prev;
	*first = 0;
	if(!p) return NULL;
	if(p_table->compare_data(data, p->data) == 0) {*first = 1; return NULL;}
	prev = p;
	p = p->next;
	while(p) {
		if(p_table->compare_data(data, p->data) == 0) return prev;
		prev = p;
		p = p->next;
	}
	return NULL;
}

// return pointer to element with given value
ht_element *get_element(hash_table *p_table, data_union *data) {
	int i = p_table->hash_function(*data, p_table->size);
	ht_element *p = p_table->ht[i];
	while(p) {
		if(p_table->compare_data(*data, p->data) == 0) return p;
		p = p->next;
	}
	return NULL;
}

// insert element
void insert_element(hash_table *p_table, data_union *data) {
	// don't insert if already present
	if(get_element(p_table, data))	return;

	ht_element *elem = safe_malloc(sizeof(ht_element));
	elem->data = *data;
	elem->next = NULL;

	int i = p_table->hash_function(*data, p_table->size);
	elem->next = p_table->ht[i];
	p_table->ht[i] = elem;
	p_table->no_elements++;

	// rehash if necessary
	if(p_table->no_elements / p_table->size > MAX_RATE) rehash(p_table);
}

// remove element
void remove_element(hash_table *p_table, data_union data) {
	int first;
	ht_element *prev = find_previous(p_table, data, &first), *p = NULL;
	if(first == 1) {
		int i = p_table->hash_function(data, p_table->size);
		p = p_table->ht[i];
		p_table->ht[i] = p->next;
	}
	else if(prev) {
		p = prev->next;
		prev->next = p->next;
	}

	if(p) {
		free_element(p_table->free_data, p);
		p_table->no_elements--;
	}
}

// type-specific definitions

// int element

int hash_int(data_union data, int size) {
	return hash_base(data.int_data, size);
}

void dump_int(data_union data) {
	printf("%d ", data.int_data);
}

int cmp_int(data_union a, data_union b) {
	return a.int_data - b.int_data;
}

// read int value and insert to the union
data_union create_data_int() {
	data_union du;
	scanf("%d", &du.int_data);
	return du;
}

// char element

int hash_char(data_union data, int size) {
	return hash_base((int)data.char_data, size);
}

void dump_char(data_union data) {
	printf("%c ", data.char_data);
}

int cmp_char(data_union a, data_union b) {
	return (int)(a.char_data - b.char_data);
}

// read char value and insert to the union
data_union create_data_char() {
	data_union du;
	scanf(" %c", &du.char_data);
	return du;
}

// Word element

typedef struct DataWord {
	char *word;
	int counter;
} DataWord;

void dump_word(data_union data) {
	DataWord* dw = data.ptr_data;
	printf("%s %d", dw->word, dw->counter);
}

void free_word(data_union data) {
	free( ((DataWord*)(data.ptr_data))->word );
	free( data.ptr_data );
}

int cmp_word(data_union a, data_union b) {
	DataWord *dw_a = a.ptr_data, *dw_b = b.ptr_data;
	return strcmp( dw_a->word, dw_b->word );
}

int hash_word(data_union data, int size) {
	int s = 0;
	DataWord *dw = data.ptr_data;
	char *p = dw->word;
	while (*p) {
		s += *p++;
	}
	return hash_base(s, size);
}

// increase the counter
void modify_word(data_union *data) {
	((DataWord*)(data->ptr_data))->counter++;
}

// allocate DataWord structure and insert to the union
data_union create_data_word(char *value) {
	data_union du;
	DataWord *dw = safe_malloc(sizeof(DataWord));
	dw->word = safe_malloc(strlen(value)+1);
	dw->counter = 1;
	strcpy(dw->word, value);
	du.ptr_data = dw;
	return du;
}

// read text, parse it to words, and insert those words to the hashtable
void stream_to_ht(hash_table *p_table, FILE *stream) {
	data_union du;
	char c = getc(stream);
	char buf[BUFFER_SIZE], *word;
	while(c!=EOF) {
		ungetc(c, stream);
		fgets(buf, BUFFER_SIZE, stream);
		word = strtok(buf, DELIMS);
		while(word) {
			for(int i=0; word[i]; ++i) word[i] = tolower(word[i]);
			du = create_data_word(word);
			ht_element *el = get_element(p_table, &du);
			if(el) {
				modify_word(&el->data);
				free_word(du);
			}
			else {
				insert_element(p_table, &du);
			}

			word = strtok(NULL, DELIMS);
		}

		c = getc(stream);
	}
}

// test primitive type list
void table_test(hash_table *p_table, int n, data_union (*create_data)()) {
	char op;
	data_union data;
	for (int i = 0; i < n; ++i) {
		scanf(" %c", &op);
		data = create_data();
		switch (op) {
			case 'r':
				remove_element(p_table, data);
				break;
			case 'i':
				insert_element(p_table, &data);
				break;
			default:
				printf("No such operation: %c\n", op);
				break;
		}
	}
}

int main(void) {
	int to_do, n, index;
	hash_table table;
	char buffer[BUFFER_SIZE], c;
	data_union data;

	scanf ("%d", &to_do);
	switch (to_do) {
		case 1: // test integer table
			scanf("%d %d",&n, &index);
			init_ht(&table, 4, dump_int,NULL,
					cmp_int, hash_int, NULL);
			table_test(&table, n, create_data_int);
			printf ("%d\n", table.size);
			dump_list(&table, index);
			free_table(&table);
			break;
		case 2: // test char table
			scanf("%d %d",&n, &index);
			init_ht(&table, 4, dump_char,NULL,
			        cmp_char, hash_char, NULL);
			table_test(&table, n, create_data_char);
			printf ("%d\n", table.size);
			dump_list(&table, index);
			free_table(&table);
			break;
		case 3: // read words from text, insert into table, and print
			scanf("%s", buffer);
			init_ht(&table, 8, dump_word, free_word,
			        cmp_word, hash_word, modify_word);
			stream_to_ht(&table, stdin);
			printf ("%d\n", table.size);
			data = create_data_word(buffer);
			ht_element *e = get_element(&table, &data);
			if (e) table.dump_data(e->data);
			if (table.free_data) table.free_data(data);
			free_table(&table);
			break;
		default:
			printf("NOTHING TO DO FOR %d\n", to_do);
			break;
	}
	return 0;
}

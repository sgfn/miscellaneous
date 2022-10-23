#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <ctype.h>
#define MAX_STR_LEN 64

typedef struct Vector {
	void *data;
	size_t element_size;
	size_t size;
	size_t capacity;
} Vector;

typedef struct Person {
	int age;
	char first_name[MAX_STR_LEN];
	char last_name[MAX_STR_LEN];
} Person;

// Allocate vector to initial capacity (block_size elements),
// Set element_size, size (to 0), capacity
void init_vector(Vector *vector, size_t block_size, size_t element_size) {
	vector->data = malloc(element_size*block_size);
	vector->element_size = element_size;
	vector->size = 0;
	vector->capacity = block_size;
}

// If new_capacity is greater than the current capacity,
// new storage is allocated, otherwise the function does nothing.
void reserve(Vector *vector, size_t new_capacity) {
	if (new_capacity > vector->capacity) {
		vector->data = realloc(vector->data, new_capacity*vector->element_size);
		vector->capacity = new_capacity;
	}
}

// Resizes the vector to contain new_size elements.
// If the current size is greater than new_size, the container is
// reduced to its first new_size elements.

// If the current size is less than new_size,
// additional zero-initialized elements are appended
void resize(Vector *vector, size_t new_size) {
	reserve(vector, new_size);
	size_t old_size = vector->size;
	vector->size = new_size;
	if (new_size > old_size) {
		char * what = vector->data; // this is disgusting, there must be a better way
		what += old_size * vector->element_size;
		memset((void*)what, 0, (new_size-old_size)*vector->element_size);
	}
}

void insert(Vector*, int, void*);

// Add element to the end of the vector
void push_back(Vector *vector, void *value) {
	insert(vector, vector->size, value);
}
	

// Remove all elements from the vector
void clear(Vector *vector) {
	resize(vector, 0);
}

// Remove the last element from the vector
void pop_back(Vector *vector) {
	resize(vector, vector->size-1);
}

// Insert new element at index (0 <= index <= size) position
void insert(Vector *vector, int index, void *value) {
	if (vector->size == vector->capacity) {
		reserve(vector, 2*vector->capacity);
	}
	char * what = vector->data;
	what += index * vector->element_size;
	if (index < vector->size) {
		memmove( (void*)(what+vector->element_size), (void*)what,
				 (vector->size-index)*vector->element_size );
	}
	memcpy((void*)what, value, vector->element_size);
	++(vector->size);
}

// Erase element at position index
void erase(Vector *vector, int index) {
	char * what = vector->data;
	what += index * vector->element_size;
	memmove( (void*)what, (void*)(what+vector->element_size),
			 (vector->size-index-1)*vector->element_size );
	--(vector->size);
}

// Erase all elements that compare equal to value from the container
void erase_value(Vector *vector, void *value, int(*cmp)(const void*, const void*)) {
	char * what = vector->data;
	for (int i=0; i<vector->size;) {
		if (cmp(value, (void*)what) == 0) {
			erase(vector, i);
		}
		else {
			what += vector->element_size;
			++i;
		}
	}
}

// Erase all elements that satisfy the predicate from the vector
void erase_if(Vector *vector, int (*predicate)(void *)) {
	char * what = vector->data;
	for (int i=0; i<vector->size;) {
		if (predicate((void*)what)) {
			erase(vector, i);
		}
		else {
			what += vector->element_size;
			++i;
		}
	}
}

// Request the removal of unused capacity
void shrink_to_fit(Vector *vector) {
	if (vector->size < vector->capacity) {
		vector->data = realloc(vector->data, vector->size*vector->element_size);
		vector->capacity = vector->size;
	}
}

// Print integer vector
void print_vector_int(Vector *vector) {
	int * p = vector->data;
	printf("%d\n", vector->capacity);
	for (int i=0; i<vector->size; ++i) {
		printf("%d ", *(p++));
	}
	printf("\n");
}

// Print char vector
void print_vector_char(Vector *vector) {
	char * p = vector->data;
	printf("%d\n", vector->capacity);
	for (int i=0; i<vector->size; ++i) {
		printf("%c ", *(p++));
	}
	printf("\n");
}

// Print vector of Person
void print_vector_person(Vector *vector) {
	Person * p = vector->data;
	printf("%d\n", vector->capacity);
	for (int i=0; i<vector->size; ++i) {
		printf("%d %s %s\n", p->age, p->first_name, p->last_name);
		++p;
	}
}

// integer comparator - increasing order
int int_cmp(const void *v1, const void *v2) {
	int i1 = *(int*)v1, i2 = *(int*)v2;
	if 		(i1 > i2)	return 1;
	else if (i1 < i2)	return -1;
	else				return 0;
}

// char comparator - lexicographical order (case sensitive)
int char_cmp(const void *v1, const void *v2) {
	char c1 = *(char*)v1, c2 = *(char*)v2;
	if 		(c1 > c2)	return 1;
	else if (c1 < c2)	return -1;
	else				return 0;
}

// Person comparator:
// Sort according to age (decreasing)
// When ages equal compare first name and then last name
int person_cmp(const void *p1, const void *p2) {
	const Person *o1 = p1, *o2 = p2;
	if (o1->age < o2->age)		return 1;
	else if (o1->age > o2->age) return -1;
	else {
		int t = strcmp(o1->first_name, o2->first_name);
		if (t != 0)		return t;
		else 			return strcmp(o1->last_name, o2->last_name);
	}
}

// predicate: check if number is even
int is_even(void *value) {
	return (*(int*)value & 1 == 0) ? 1 : 0;
}

// predicate: check if char is a vowel
int is_vowel(void *value) {
	char vowels[] = {'a', 'e', 'i', 'o', 'u', 'y', 'A', 'E', 'I', 'O', 'U', 'Y'};
	for (int i=0; i<12; ++i) {
		if (*(char*)value == vowels[i])		return 1;
	}
	return 0;
}

// predicate: check if person is older than 25
int is_older_than_25(void *person) {
	return (((Person*)person)->age > 25) ? 1 : 0;
}

// -------------------------------------------------------------

void read_int(void* value) {
	scanf("%d", (int*)value);
}

void read_char(void* value) {
	char c[2];
	scanf("%s", c);
	*(char*)value = c[0];
}

void read_person(void* value) {
	Person *person = (Person*)value;
	scanf("%d %s %s", &person->age, person->first_name, person->last_name);
}

void vector_test(Vector *vector, int n, void(*read)(void*),
		 int (*cmp)(const void*, const void*), int(*predicate)(void*)) {
	char op[2];
	int index;
	size_t size;
	void *v = malloc(vector->element_size);
	for (int i = 0; i < n; ++i) {
		scanf("%s", op);
		switch (op[0]) {
			case 'p': // push_back
				read(v);
				push_back(vector, v);
				break;
			case 'i': // insert
				scanf("%d", &index);
				read(v);
				insert(vector, index, v);
				break;
			case 'e': // erase
				scanf("%d", &index);
				read(v);
				erase(vector, index);
				erase_value(vector, v, cmp);
				break;
			case 'd': // erase (predicate)
				erase_if(vector, predicate);
				break;
			case 'r': // resize
				scanf("%zu", &size);
				resize(vector, size);
				break;
			case 'c': // clear
				clear(vector);
				break;
			case 'f': // shrink
				shrink_to_fit(vector);
				break;
			case 's': // sort
				qsort(vector->data, vector->size,
				      vector->element_size, cmp);
				break;
			default:
				printf("No such operation: %s\n", op);
				break;
		}
	}
	free(v);
}

int main(void) {
	int to_do, n;
	Vector vector_int, vector_char, vector_person;

	scanf("%d%d", &to_do, &n);

	switch (to_do) {
		case 1:
			init_vector(&vector_int, 4, sizeof(int));
			vector_test(&vector_int, n, read_int, int_cmp, is_even);
			print_vector_int(&vector_int);
			free(vector_int.data);
			break;
		case 2:
			init_vector(&vector_char, 2, sizeof(char));
			vector_test(&vector_char, n, read_char, char_cmp, is_vowel);
			print_vector_char(&vector_char);
			free(vector_char.data);
			break;
		case 3:
			init_vector(&vector_person, 2, sizeof(Person));
			vector_test(&vector_person, n, read_person, person_cmp, is_older_than_25);
			print_vector_person(&vector_person);
			free(vector_person.data);
			break;
		default:
			printf("Nothing to do for %d\n", to_do);
			break;
	}

	return 0;
}


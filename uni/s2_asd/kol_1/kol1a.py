"""
Jakub Pisarek

Rozwiązanie polega na wzięciu napisu wcześniejszego leksykograficznie spośród
jego wersji od tyłu i od przodu, posortowaniu tychże napisów (rozdzielonych do 
bucketów wg ich długości) radix sortem, finalnie na przejściu liniowo przez
wynikowe buckety w poszukiwaniu najdłuższego spójnego stałego podciągu.

Złożoność czasowa algorytmu wynosi O(N)
Złożoność pamięciowa algorytmu wynosi O(N)
"""

from kol1atesty import runtests


def radix_sort(T, str_len):
    n = len(T)
    k = 26
    for sort_key in range(str_len-1, -1, -1):
        # Counting sort
        C = [0 for _ in range(k)]
        B = [None for _ in T]

        for el in T:
            letter_index = ord(el[sort_key])-ord('a')
            C[letter_index] += 1

        for i in range(1, k):   C[i] += C[i-1]

        for i in range(n-1, -1, -1):
            letter_index = ord(T[i][sort_key])-ord('a')
            B[C[letter_index]-1] = T[i]
            C[letter_index] -= 1

        for i in range(n):
            T[i] = B[i]
    return T


def g(T):
    max_len = 0
    min_len = 10**100

    for el in T: # O(n)
        max_len = max(len(el), max_len)
        min_len = min(len(el), min_len)

    buckets = [[] for _ in range(min_len, max_len+1)] # O(N)

    for el in T: # O(n)
        buckets[len(el)-min_len].append(el)

    ans = 1
    for i, bucket in enumerate(buckets): # O(N)
        if len(bucket) > 1:
            for j, str_fwd in enumerate(bucket):
                str_rev = str_fwd[::-1]
                bucket[j] = str_fwd if str_fwd < str_rev else str_rev
            radix_sort(bucket, i+min_len)
            prev_str = bucket[0]
            curr = 1
            for j in range(1, len(bucket)):
                if prev_str == bucket[j]:
                    curr += 1
                else:
                    ans = max(ans, curr)
                    curr = 1
                prev_str = bucket[j]
            ans = max(ans, curr)
    
    return ans


# Zamien all_tests=False na all_tests=True zeby uruchomic wszystkie testy
runtests( g, all_tests=True )

"""
Jakub Pisarek

Rozwiązanie bazuje na zmodyfikowanym algorytmie sortowania kubełkowego (bucket
sort). Tworzonych jest n//8 kubełków (wartość wyznaczona eksperymentalnie),
każdy ze średnio 8 elementami, które, po przydzieleniu do nich wartości, są sor-
towane hybrydowym algorytmem quicksort+insertion sort.

Złożoność czasowa algorytmu wynosi pesymistycznie O(n log n), dla rozkładu
jednostajnego - O(n). W funkcji linear_SortTab() została zaimplementowana wersja
algorytmu działająca zawsze w czasie liniowym, która jednak, z racji na gorszą
stałą, nie przechodzi wszystkich dostarczonych testów. W związku z tym zdecy-
dowałem się na pozostawienie algorytmu o gorszej pesymistycznej złożoności.

Złożoność pamięciowa (dodatkowej pamięci) algorytmu wynosi O(n).

W kilku miejscach programu występują te same fragmenty kodu. Nie zostały one
przeniesione do osobnych funkcji z racji na specyfikę języka Python
(kosztowne, powolne wykonywanie wszystkich funkcji, brak funkcji inline).

Komentarze autora (tj. moje) wewnątrz kodu zostały wykonane w jęz. angielskim.
"""

from zad3testy import runtests

def linear_SortTab(T,P):
    """Linear version. Not used due to poor constant."""

    QS_THRESHOLD = 20   # Threshold for using the quicksort algorithm
    STACK_SIZE = 24     # Function call stack size

    qs_stack = [None for _ in range(STACK_SIZE)]
    qs_top = 0

    N = len(T)
    big_buckets = [[] for _ in T]

    for el in T:
        big_buckets[int(el) if el != N else N-1].append(el)

    for i, big_bucket in enumerate(big_buckets):
        b_n = len(big_bucket)
        if b_n < 2:     continue

        b_n >>= 3
        if b_n == 0:    b_n = 1

        small_buckets = [[] for _ in range(b_n)]

        for el in big_bucket:
            index = int((el-i)*b_n) if el!=i+1 else b_n-1
            small_buckets[index].append(el)  

        i_b = 0
        for bucket in small_buckets:
            l_bucket = len(bucket)
            if l_bucket > 1:    # bucket needs to be sorted
                # Use insertion sort for small subarrays
                if l_bucket < QS_THRESHOLD:
                    i = 1
                    while i < l_bucket:
                        x = bucket[i]
                        j = i - 1
                        while j >= 0 and bucket[j] > x:
                            bucket[j+1] = bucket[j]
                            j -= 1
                        bucket[j+1] = x
                        i += 1
                
                # Use quicksort for larger subarrays
                else:
                    qs_stack[0] = (0, l_bucket-1)
                    qs_top = 1
                    while qs_top > 0:
                        qs_top -= 1
                        left, right = qs_stack[qs_top]
                        pivot = bucket[(left+right)>>1] # should be ok-ish

                        i = left
                        j = right
                        while i <= j:
                            while bucket[i] < pivot:
                                i += 1
                            while bucket[j] > pivot:
                                j -= 1
                            if i <= j:
                                bucket[i], bucket[j] = bucket[j], bucket[i]
                                i += 1
                                j -= 1

                        if left < j:
                            # If both ranges are to be considered, handle the 
                            # shorter one first, as that minimises the risk of a
                            # stack overflow
                            if i < right:
                                if right-i > j-left:
                                    qs_stack[qs_top] = (i, right)
                                    qs_stack[qs_top+1] = (left, j)
                                else:
                                    qs_stack[qs_top] = (left, j)
                                    qs_stack[qs_top+1] = (i, right)
                                qs_top += 2
                            else:
                                qs_stack[qs_top] = (left, j)
                                qs_top += 1
                        elif i < right:
                            qs_stack[qs_top] = (i, right)
                            qs_top += 1
        
            for el in bucket:
                big_bucket[i_b] = el
                i_b += 1

    i_curr = 0
    for big_bucket in big_buckets:
        for el in big_bucket:
            T[i_curr] = el
            i_curr += 1

    return T


def bucket_sort(T, b_amnt, r_beg, r_end):
    QS_THRESHOLD = 20   # Threshold for using the quicksort algorithm
    STACK_SIZE = 24     # Function call stack size

    # Create a function call stack for the quicksort algorithm
    qs_stack = [None for _ in range(STACK_SIZE)]    # Mem. compl.: O(1)
    qs_top = 0

    # Create the needed amount of buckets
    if b_amnt == 0:      b_amnt = 1
    buckets = [[] for _ in range(b_amnt)]    # Mem. compl.: O(n)

    # Fill the buckets with appropriate values
    for el in T:    # Time compl.: O(n)
        index = int((el-r_beg)/(r_end-r_beg)*b_amnt) if el!=r_end else b_amnt-1
        buckets[index].append(el)

    i_curr = 0

    # Sort each bucket and write to T
    for bucket in buckets:  # Time compl.: avg O(n), worst-case O(n log n)
        l_bucket = len(bucket)
        if l_bucket > 1:    # Bucket needs to be sorted
            # Use insertion sort for small subarrays
            if l_bucket < QS_THRESHOLD:
                i = 1
                while i < l_bucket:
                    x = bucket[i]
                    j = i - 1
                    while j >= 0 and bucket[j] > x:
                        bucket[j+1] = bucket[j]
                        j -= 1
                    bucket[j+1] = x
                    i += 1
            
            # Use quicksort for larger subarrays
            else:
                qs_stack[0] = (0, l_bucket-1)
                qs_top = 1
                while qs_top > 0:
                    qs_top -= 1
                    left, right = qs_stack[qs_top]
                    pivot = bucket[(left+right)>>1] # should be decent enough

                    i = left
                    j = right
                    while i <= j:
                        while bucket[i] < pivot:
                            i += 1
                        while bucket[j] > pivot:
                            j -= 1
                        if i <= j:
                            bucket[i], bucket[j] = bucket[j], bucket[i]
                            i += 1
                            j -= 1

                    if left < j:
                        # If both ranges are to be considered, handle the 
                        # shorter one first, as that minimises the risk of a
                        # stack overflow
                        if i < right:
                            if right-i > j-left:
                                qs_stack[qs_top] = (i, right)
                                qs_stack[qs_top+1] = (left, j)
                            else:
                                qs_stack[qs_top] = (left, j)
                                qs_stack[qs_top+1] = (i, right)
                            qs_top += 2
                        else:
                            qs_stack[qs_top] = (left, j)
                            qs_top += 1
                    elif i < right:
                        qs_stack[qs_top] = (i, right)
                        qs_top += 1

        # Overwrite the values in T
        for el in bucket:
            T[i_curr] = el
            i_curr += 1
    return T


def SortTab(T,P):
    # return linear_SortTab(T,P)

    n = len(T)

    r_begin = n+1
    r_end = 0
    for b, e, prob in P: # Get union of all ranges
        r_begin = min(r_begin, b)
        r_end = max(r_end, e)

    return bucket_sort(T, n>>3, r_begin, r_end) # n//8 chosen by trial-and-error


runtests( SortTab )

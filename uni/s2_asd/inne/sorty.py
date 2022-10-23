from random import randint


def quicksort(T):
    qstack = [(0, len(T)-1)]
    while len(qstack) > 0:
        left, right = qstack.pop()

        # pivot = T[(left+right)>>1]
        # Alternatively: choosing a pivot as median of three elements
        el1 = T[left]
        el2 = T[right]
        el3 = T[(left+right)>>1]
        if el1 < el2:
            if      el2 < el3:      pivot = el2
            elif    el1 < el3:      pivot = el3
            else:                   pivot = el1
        else:
            if      el1 < el3:      pivot = el1
            elif    el2 < el3:      pivot = el3
            else:                   pivot = el2

        i = left
        j = right
        while i <= j:
            while T[i] < pivot:
                i += 1
            while pivot < T[j]:
                j -= 1
            if i <= j:
                T[i], T[j] = T[j], T[i]
                i += 1
                j -= 1
        if left < j:
            if i < right:
                if j - left > right - i:
                    qstack.extend(((left, j), (i, right)))
                else:
                    qstack.extend(((i, right), (left, j)))
            else:
                qstack.append((left, j))
        elif i < right:
            qstack.append((i, right))
    return T


def heapsort(T):
    parent = lambda x: (x-1)//2
    left = lambda x: 2*x+1
    right = lambda x: 2*x+2

    n = len(T)
    if n < 2:       return T
    first_incorrect = parent(n-1)
    
    for i in range(first_incorrect, -1, -1):
        t = i
        while True:     # down-heapify
            max_ind = t
            l = left(t)
            r = right(t)
            if l < n and T[l] > T[max_ind]:
                max_ind = l
            if r < n and T[r] > T[max_ind]:
                max_ind = r

            if max_ind != t:
                T[t], T[max_ind] = T[max_ind], T[t]
                t = max_ind
            else:
                break
    
    for i in range(n-1, 0, -1):
        T[i], T[0] = T[0], T[i]
        t = 0
        while True:     # down-heapify
            max_ind = t
            l = left(t)
            r = right(t)
            if l < i and T[l] > T[max_ind]:
                max_ind = l
            if r < i and T[r] > T[max_ind]:
                max_ind = r

            if max_ind != t:
                T[t], T[max_ind] = T[max_ind], T[t]
                t = max_ind
            else:
                break
    
    return T


def counting_sort(T, k):
    # Assuming T contains integers from the [0, k-1] range
    n = len(T)
    counters = [0 for _ in range(k)]
    t_out = [None for _ in T]

    for el in T:            counters[el] += 1
    for i in range(1, k):   counters[i]  += counters[i-1]
    for i in range(n-1, -1, -1):
        t_out[counters[T[i]]-1] = T[i]
        counters[T[i]] -= 1
    
    for i in range(n):
        T[i] = t_out[i]
    return T


def bucket_sort(T, r_begin, r_end):
    n = len(T)
    buckets = [[] for _ in range(n)]
    for el in T:
        index = int((el-r_begin)/(r_end-r_begin)*n)
        buckets[index].append(el)
    
    i_curr = 0
    for bucket in buckets:
        if len(bucket) > 1:
            quicksort(bucket)
        for el in bucket:
            T[i_curr] = el
            i_curr += 1

    return T


def radix_sort(T):
    n = len(T)
    el_len = len(T[0])  # Assuming all strings are the same length
    for i in range(el_len-1, -1, -1):
        # Modified counting sort
        C = [0 for _ in range(26)]
        B = [None for _ in T]
        
        for el in T:
            letter_index = ord(el[i])-ord('a')
            C[letter_index] += 1
        
        for j in range(1, 26):
            C[j] += C[j-1]
        
        for j in range(n-1, -1, -1):
            letter_index = ord(T[j][i])-ord('a')
            B[C[letter_index]-1] = T[j]
            C[letter_index] -= 1
        
        for j in range(n):
            T[j] = B[j]
    
    return T


def quickselect(T, index):
    left, right = 0, len(T)-1
    while True:
        if left == right:
            return T[left]
        if left < right:
            # PARTITION - wersja z wykładu
            rand_ind = randint(left, right)
            T[right], T[rand_ind] = T[rand_ind], T[right]
            pivot = T[right]
            i = left - 1
            for j in range(left, right):
                if T[j] <= pivot:
                    i += 1
                    T[i], T[j] = T[j], T[i]
            T[i+1], T[right] = T[right], T[i+1]
            q = i+1

            if q == index:
                return T[q]
            elif q < index:
                left = q+1
            else:
                right = q-1
        else:
            return -1


def binsearch(T, val):
    left = 0
    right = len(T)-1
    while left <= right:
        mid = (left+right)>>1
        if T[mid] == val:
            return True
        elif T[mid] > val:
            right = mid-1
        else:
            left = mid+1
    return False


def insertion_sort(T, left=None, right=None):
    if left is None:        left, right = 0, len(T)-1
    i = left + 1
    while i <= right:
        x = T[i]
        j = i-1
        while j >= 0 and T[j] > x:
            T[j+1] = T[j]
            j -= 1
        T[j+1] = x
        i += 1


def two_pointers_trick(T, x):
    # For instance, check if there exist such two elements in sorted tab T, 
    # under indices i and j, i<>j, that T[j]-T[i] = x  (x>0)
    n = len(T)
    i = 0
    j = 1
    while i<n and j<n:
        diff = T[j]-T[i]
        if diff == x:
            return (i, j)
        elif diff < x:
            j += 1
        else:
            i += 1
    return (-1, -1)


if __name__ == '__main__':
    T = [randint(1, 1000) for _ in range(20)]
    print(T)

    # for i in (0, 12, 24):
    #     print(quickselect(T, i))

    heapsort(T)
    # counting_sort(T, 1001)
    # bucket_sort(T, 1, 1001)
    # insertion_sort(T)
    print(T)

    print(two_pointers_trick(T, 100))

    # S = ["trakt", "krasa", "lemat", "artis", "retro", "udane", "polot", "kitel", 
    #      "stoki", "trasy", "kiler", "zuchy", "sklep", "mnich", "baran", "karta", 
    #      "forty", "kefir", "krata", "ataki", "chaos", "tatar", "taras", "zebra"]
    # radix_sort(S)
    # print(S)

    # T = [1, 1, 3, 5, 6, 11, 13, 13, 13, 29, 30, 31, 31, 38, 42]
    # for test in (1, 2, 3, 6, 10, 0, 16, 29, 38, 55):
    #     print(binsearch(T, test))

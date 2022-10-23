# Jakub Pisarek
# 
# Rozwiązanie jest hybrydowe, wykorzystuje trzy różne algorytmy w zależności od
# rzędu wielkości parametru k<=n. Gdy:
#    k=1          Wykonuje pojedyncze przejście algorytmu sortowania bąbelkowego
#                 (bubblesort), co jest wystarczające do posortowania listy.
#                     Złożoność czasowa: O(n), pamięciowa: O(1);
#    1<k<256      Sortuje listę algorytmem sortowania kopcowego (heapsort),
#                 z użyciem dodatkowej tablicy o rozmiarze k jako kopca,
#                 do którego wkłada k pierwszych wartości, a następnie wykonuje
#                 operację wstawienia-wyjęcia (insert-extract) dla wszystkich 
#                 pozostałych elementów listy, co pozwala na jej posortowanie.
#                     Złożoność czasowa: O(n log k), pamięciowa: O(k);
#    256<=k       Sortuje listę algorytmem sortowania przez scalanie (mergesort)
#                     Złożoność czasowa: O(n log n), pamięciowa: O(1).
# 
# W kilku miejscach programu występują te same fragmenty kodu. Nie zostały one
# przeniesione do osobnych funkcji z racji na specyfikę języka Python
# (kosztowne, powolne wykonywanie wszystkich funkcji, brak funkcji inline).
# 
# Komentarze autora (tj. moje) wewnątrz kodu zostały wykonane w jęz. angielskim.

from zad1testy import Node, runtests


def ll_msort(p, length):
    """
    Sort a linked list (without a sentinel node) of given length pointed to by p
    using the mergesort algorithm (recursive version).
    Returns a pointer to the first node of the list.
    """
    # Handle base cases
    if length <= 2:
        # Stop the recursion if list is empty or has a single node
        if length < 2:
            return p
        # Quickly handle a base case: list has exactly two nodes
        q = p.next
        if p.val > q.val:
            q.next = p
            p.next = None
            return q
        else:
            return p

    # Create pointers for the nodes in front and in the middle of the list
    p_start = p
    p_middle_prev = p
    
    # Find the middle node of the list
    for _ in range((length>>1)-1):
        p_middle_prev = p_middle_prev.next
    p_middle = p_middle_prev.next
    
    # Unlink the two halves of the list
    p_middle_prev.next = None
    
    # Recursively sort the smaller lists
    p = ll_msort(p_start, length>>1)
    q = ll_msort(p_middle, length>>1 if length&1 == 0 else (length>>1)+1)

    # MERGE THE SORTED LISTS
    # Check validity of pointers
    if p is None:
        return q
    if q is None:
        return p

    # Create a pointer to the starting node
    if p.val < q.val:
        p_start = p
        p = p.next
    else:
        p_start = q
        q = q.next
    p_curr = p_start

    # Keep adding the lowest-valued node to the end of the list
    while p is not None and q is not None:
        if p.val < q.val:
            p_curr.next = p
            p_curr = p
            p = p.next
        else:
            p_curr.next = q
            p_curr = q
            q = q.next
    
    # Add the remaining nodes from one of the lists
    if p is not None:
        p_curr.next = p
    elif q is not None:
        p_curr.next = q
    
    # Return a pointer to the first node
    return p_start


def ll_k_hsort(p, k):
    """
    Sort a k-chaotic linked list (without a sentinel node) pointed to by p
    using the k-heapsort algorithm (heap size: k).
    Returns a pointer to the first node of the list.
    """
    # Create a sentinel node, a pointer to the current node and the heap
    s = Node()
    p_curr = s
    heap = [None for _ in range(k)]
    
    # Construct a binary min-heap from the first k nodes (time compl.: O(k))
    first_incorrect = (k-1 - 1) >> 1
    for i in range(k-1, first_incorrect, -1):
        heap[i] = p
        p = p.next
    for i in range(first_incorrect, -1, -1):
        heap[i] = p
        p = p.next
        # down-heapify
        while True:
            l = (i<<1) + 1
            r = (i<<1) + 2
            max_ind = i
            if l < k and heap[max_ind].val > heap[l].val:
                max_ind = l
            if r < k and heap[max_ind].val > heap[r].val:
                max_ind = r
            if max_ind != i:
                heap[i], heap[max_ind] = heap[max_ind], heap[i]
                i = max_ind
            else:
                break

    # Perform insert-extract operations for each remaining node
    #       (time compl.: O((n-k)*log k))
    while p is not None:
        if p.val < heap[0].val:
            p_curr.next = p         # add p to the list, don't modify heap
        else:
            p_curr.next = heap[0]   # add root of heap to the list
            heap[0] = p             # replace the root
            # down-heapify
            i = 0
            while True:
                l = (i<<1) + 1
                r = (i<<1) + 2
                max_ind = i
                if l < k and heap[max_ind].val > heap[l].val:
                    max_ind = l
                if r < k and heap[max_ind].val > heap[r].val:
                    max_ind = r
                if max_ind != i:
                    heap[i], heap[max_ind] = heap[max_ind], heap[i]
                    i = max_ind
                else:
                    break
        p_curr = p_curr.next
        p = p.next
    
    # Add the remaining k elements to the list (time compl.: O(k*log k))
    for last in range(k-1, -1, -1):
        p_curr.next = heap[0]
        heap[0] = heap[last]
        # down-heapify
        i = 0
        while True:
            l = (i<<1) + 1
            r = (i<<1) + 2
            max_ind = i
            if l < last and heap[max_ind].val > heap[l].val:
                max_ind = l
            if r < last and heap[max_ind].val > heap[r].val:
                max_ind = r
            if max_ind != i:
                heap[i], heap[max_ind] = heap[max_ind], heap[i]
                i = max_ind
            else:
                break
        p_curr = p_curr.next

    # Unlink the last node from anything it might've been linked to
    p_curr.next = None

    # Destroy the sentinel node, return a pointer to the first node
    p = s.next
    del s
    return p


def SortH(p,k):
    # List is 0-chaotic (already sorted)
    if k == 0:
        pass

    # List is 1-chaotic - apply a single pass of bubblesort (time compl.: O(n))
    elif k == 1:
        # Create a sentinel node
        s = Node()
        s.next = p
        p_prev = s

        # Swap two adjacent nodes if necessary (it's enough to sort the list)
        while p is not None:
            q = p.next
            if q is not None and p.val > q.val:
                p_prev.next = q
                p.next = q.next
                q.next = p
            # If p and q were swapped, checking q with q.next can be omitted
            p_prev = p
            p = p.next
    
        # Destroy the sentinel node, return a pointer to the first actual node
        p = s.next
        del s

    # List is at best 2-chaotic
    else:
        # Calculate length of list (necessary to avoid runtime errors with k>n)
        s = p
        n = 0
        while p is not None:
            n += 1
            p = p.next

        # 1<k<256, k<=n - apply k-heapsort (time compl.: O(n log k))
        #       (256 was picked semi-randomly as around that point
        #       k-heapsort starts to perform worse than mergesort)
        if k <= n and k < 256:
            p = ll_k_hsort(s, k)

        # 256>=k or k>n - apply mergesort  (time compl.: O(n log n))
        else:
            p = ll_msort(s, n)

    # Return a pointer to the first node
    return p


runtests( SortH ) 

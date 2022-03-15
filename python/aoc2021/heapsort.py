from random import randint


def heapify(*args, reverse=False, structures=False, str_ind=0):
    n = len(args)
    heap = [0 for _ in range(n)]
    for i, arg in enumerate(args):
        heap[i] = arg
        if structures:
            if reverse:
                while i != 0 and heap[i][str_ind] < heap[(i-1)//2][str_ind]:
                    heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                    i = (i-1)//2
            else:
                while i != 0 and heap[i][str_ind] > heap[(i-1)//2][str_ind]:
                    heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                    i = (i-1)//2

        else:
            if reverse:
                while i != 0 and heap[i] < heap[(i-1)//2]:
                    heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                    i = (i-1)//2
            else:
                while i != 0 and heap[i] > heap[(i-1)//2]:
                    heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                    i = (i-1)//2
    return heap


def heap_insert(heap, arg, reverse=False, structures=False, str_ind=0):
    # treating list as list, not as array
    heap.append(arg)
    i = len(heap)-1
    if structures:
        if reverse:
            while i != 0 and heap[i][str_ind] < heap[(i-1)//2][str_ind]:
                heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                i = (i-1)//2
        else:
            while i != 0 and heap[i][str_ind] > heap[(i-1)//2][str_ind]:
                heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                i = (i-1)//2

    else:
        if reverse:
            while i != 0 and heap[i] < heap[(i-1)//2]:
                heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                i = (i-1)//2
        else:
            while i != 0 and heap[i] > heap[(i-1)//2]:
                heap[i], heap[(i-1)//2] = heap[(i-1)//2], heap[i]
                i = (i-1)//2
    return


def heap_extract(heap, reverse=False, structures=False, str_ind=0):
    n = len(heap)-1
    val = heap[0]
    heap[0] = heap[-1]
    heap.pop()
    i = 0

    if structures:
        if reverse:
            while i*2 + 2 < n and (heap[i][str_ind] > heap[i*2 + 1][str_ind]
                                   or heap[i][str_ind] > heap[i*2 + 2][str_ind]):
                if heap[i*2 + 2][str_ind] < heap[i*2 + 1][str_ind]:
                    heap[i*2 + 2], heap[i] = heap[i], heap[i*2 + 2]
                    i = i*2 + 2
                else:
                    heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]
                    i = i*2 + 1
            if i*2 + 1 < n and heap[i][str_ind] > heap[i*2 + 1][str_ind]:
                heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]

        else:
            while i*2 + 2 < n and (heap[i][str_ind] < heap[i*2 + 1][str_ind]
                                   or heap[i][str_ind] < heap[i*2 + 2][str_ind]):
                if heap[i*2 + 2][str_ind] > heap[i*2 + 1][str_ind]:
                    heap[i*2 + 2], heap[i] = heap[i], heap[i*2 + 2]
                    i = i*2 + 2
                else:
                    heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]
                    i = i*2 + 1
            if i*2 + 1 < n and heap[i][str_ind] < heap[i*2 + 1][str_ind]:
                heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]

    else:
        if reverse:
            while i*2 + 2 < n and (heap[i] > heap[i*2 + 1]
                                   or heap[i] > heap[i*2 + 2]):
                if heap[i*2 + 2] < heap[i*2 + 1]:
                    heap[i*2 + 2], heap[i] = heap[i], heap[i*2 + 2]
                    i = i*2 + 2
                else:
                    heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]
                    i = i*2 + 1
            if i*2 + 1 < n and heap[i] > heap[i*2 + 1]:
                heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]

        else:
            while i*2 + 2 < n and (heap[i] < heap[i*2 + 1]
                                   or heap[i] < heap[i*2 + 2]):
                if heap[i*2 + 2] > heap[i*2 + 1]:
                    heap[i*2 + 2], heap[i] = heap[i], heap[i*2 + 2]
                    i = i*2 + 2
                else:
                    heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]
                    i = i*2 + 1
            if i*2 + 1 < n and heap[i] < heap[i*2 + 1]:
                heap[i*2 + 1], heap[i] = heap[i], heap[i*2 + 1]
    return val


def heapsort(*args, ascending=True, structures=False, str_ind=0):
    '''
    Will sort the items in ascending order by default, this behaviour can be
    changed by setting the flag ascending=False; works on separate int/float
    values by default, set the flag structures=True to make it work on the first
    element of a list/tuple.
    '''
    heap = heapify(*args, reverse=ascending, structures=structures,
                   str_ind=str_ind)
    ans = []
    while len(heap) > 0:
        ans.append(heap_extract(heap, reverse=ascending, structures=structures,
                                str_ind=str_ind))
    return ans


def bubblesort(*args):
    # unrelated, for testing and comparison purposes only
    ans = list(args)
    n = len(ans)
    sorted_flag = False
    while not sorted_flag:
        sorted_flag = True
        for i in range(n-1):
            if ans[i] < ans[i+1]:
                ans[i+1], ans[i] = ans[i], ans[i+1]
                sorted_flag = False
    return ans


if __name__ == '__main__':
    to_sort = [[randint(1, 99), 's'+str(randint(10000, 99999))]
               for _ in range(20)]
    print(to_sort)
    print()
    print(heapsort(*to_sort, ascending=False, structures=True))
    # bubblesort(*to_sort)

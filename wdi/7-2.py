class Node():
    def __init__(self):
        self.val = None
        self.index = None
        self.next = None


class SparseArray():
    def __init__(self):
        s = Node()
        s.index = -1

        self.first = s
        self.len = 0


def arr_init(*vals):
    array = SparseArray()
    p = array.first
    for ind, val in enumerate(vals):
        if val != 0:
            q = Node()
            q.val = val
            q.index = ind
            p.next = q
            p = q
    array.len = len(vals)
    return array


def arr_get(array, i):
    if i < 0 or i >= array.len:
        raise IndexError
    p = array.first.next
    while p != None:
        if p.index == i:
            return p.val
        elif p.index > i:
            return 0
        p = p.next
    return 0


def arr_set(array, i, val):
    if i < 0 or i >= array.len:
        raise IndexError
    p = array.first.next
    q = array.first
    while p != None:
        if p.index == i:
            p.val = val
            return
        elif p.index > i:
            break
        q = p
        p = p.next
    r = Node()
    r.val = val
    r.index = i
    q.next = r
    r.next = p


def arr_print(array):
    p = array.first.next
    print('[', end='')
    i = -1
    while p != None:
        print('0, ' * (p.index-i-1), end='')
        print(p.val, end=', ' if p.index != array.len-1 else '')
        i = p.index
        p = p.next
    if i != array.len-1:
        print('0, ' * (array.len-i-2), '0', sep='', end='')
    print(']')


if __name__ == '__main__':
    array = arr_init(0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 3, 5, 0, 0, 0, 7, 0, 0, 0, 0,
                     0, 0, 11, 0, 0, 13, 17, 0, 0, 0, 0, 0, 0, 0, 19, 23, 0)
    arr_print(array)
    print(arr_get(array, 0))
    print(arr_get(array, 11))
    try:
        print(arr_get(array, 37))
    except IndexError:
        print('raised IndexError')
    arr_set(array, 0, 1500)
    arr_set(array, 36, -1)
    arr_set(array, 2, 28733)
    arr_print(array)
    try:
        arr_set(array, 101, 3)
    except IndexError:
        print('raised IndexError')

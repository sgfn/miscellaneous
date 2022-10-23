class Node():
    def __init__(self):
        self.val = None
        self.next = None


def set_init():
    return Node()


def set_contains(p, val):
    while p.next != None and (p.val == None or p.val < val):
        p = p.next
    if p.val == val:
        return True
    return False


def set_insert(p, val):
    while p.next != None and (p.val == None or p.val < val):
        t = p
        p = p.next
    if p.val == val:
        return
    q = Node()
    q.val = val
    if p.val != None:
        q.next = p
        t.next = q
    else:
        p.next = q


def set_extend(s, *vals):
    for val in vals:
        set_insert(s , val)


def set_remove(p, val):
    while p.next != None and (p.val == None or p.val < val):
        t = p
        p = p.next
    if p.val == val:
        t.next = p.next
        del p
    else:
        return 1


def set_print(p):
    print('{', end='')
    while p.next != None:
        p = p.next
        print(p.val, end=', ' if p.next != None else '')
    print('}')


if __name__ == '__main__':
    s = set_init()
    set_print(s)
    set_insert(s, 15)
    set_print(s)
    print(set_contains(s, 15))
    print(set_contains(s, 20))
    set_extend(s, 5, 4, 6, 2, 0, 11, 13, 3, 2, 7, 1, 11, 5, 3, 5)
    set_print(s)
    print(set_contains(s, 12321))
    print(set_contains(s, -1))
    print(set_contains(s, 11))
    set_remove(s, 5)
    set_print(s)
    set_remove(s, 3)
    set_print(s)
    set_remove(s, 42)
    set_print(s)

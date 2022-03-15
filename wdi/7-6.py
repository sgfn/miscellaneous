class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def make_list(*args):
    s = Node(args[0])
    p = s
    for i in range(1, len(args)):
        q = Node(args[i])
        p.next = q
        p = p.next
    return s


def print_list(s):
    p = s
    print('[', end='')
    while p is not None:
        print(p.val, end=', ' if p.next is not None else '')
        p = p.next
    print(']')


def insert(s, val):
    q = Node(val)
    if s is None:
        s = q
    else:
        while s is not None:
            t = s
            s = s.next
        t.next = q
    return s


if __name__ == '__main__':
    # s = make_list()
    s = None
    print_list(s)
    s = insert(s, 15)
    insert(s, 20)
    print_list(s)
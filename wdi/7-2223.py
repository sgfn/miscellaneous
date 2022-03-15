class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def make_cycle_list(cycle_len=0, *args):
    s = Node(args[0])
    p = s
    c = None
    for i in range(1, len(args)):
        q = Node(args[i])
        if i == len(args) - cycle_len:
            c = q
        p.next = q
        p = p.next
    if c is not None:
        p.next = c
    return s


def print_list(s, limit=10**100):
    p = s
    print('[', end='')
    i = 0
    while p is not None and i <= limit:
        print(p.val, end=', ' if p.next is not None else '')
        p = p.next
        i += 1
    print(']')


def cycle_len(s):
    p = s
    i = 0
    while p is not None:
        q = s
        j = 0
        while j < i:
            if q == p:
                return i-j
            q = q.next
            j += 1
        p = p.next
        i += 1
    return 0


if __name__ == '__main__':
    s = make_cycle_list(4, 2, 3, 5, 7, 9, 11, 9, 11, 9, 11, 13)
    # print_list(s, 10)
    print(cycle_len(s))

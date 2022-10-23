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


def uniq(s):
    p = s
    d = {}
    while p is not None:
        d.setdefault(p.val, 0)
        d[p.val] += 1
        p = p.next

    p = s
    q = None
    i = 0
    while p is not None:
        if d[p.val] > 1:
            if q is not None:
                q.next = p.next
            else:
                s = p.next
            t = p.next
            del p
            p = t
        else:
            q = p
            p = p.next
        i += 1
    return s


if __name__ == '__main__':
    s = make_list(1, 2, 3, 4, 100, 5, 10, 15, 23, 242, 333)
    # print_list(s)
    s = uniq(s)
    print_list(s)
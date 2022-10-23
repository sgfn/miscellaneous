# zbiór mnogościowy, należy utworzyć listę odsyłaczową z iloczynem 3 zbiorów

# następująca definicja jest podana:
class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


def create_linklist(*args):
    s = Node(args[0]) if len(args) > 0 else None
    p = s
    for arg in args[1:]:
        p.next = Node(arg)
        p = p.next
    return s


def print_linklist(s):
    while s != None:
        print(s.val, end=' ')
        s = s.next
    print()


def product_of_three_sets(s1, s2, s3):
    if s1 == None or s2 == None or s3 == None:
        return None
    s = Node(None)
    p = s
    while s1 != None and s2 != None and s3 != None:
        if s1.val == s2.val == s3.val:
            q = Node(s1.val)
            p.next = q
            p = q
            s1 = s1.next
            s2 = s2.next
            s3 = s3.next
        else:
            min_val = min(s1.val, s2.val, s3.val)
            if s1.val == min_val:
                s1 = s1.next
            if s2.val == min_val:
                s2 = s2.next
            if s3.val == min_val:
                s3 = s3.next
    s = s.next
    return s


if __name__ == '__main__':
    s1 = create_linklist(1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 15, 20, 25, 30)
    s2 = create_linklist(2, 3, 4, 5, 6, 9, 10)
    s3 = create_linklist(1, 2, 3, 5, 7, 9, 11, 13)
    print_linklist(s1)
    print_linklist(s2)
    print_linklist(s3)
    aa = product_of_three_sets(s1, s2, s3)
    print_linklist(aa)
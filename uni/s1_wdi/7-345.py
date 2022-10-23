from random import randint


class Node:
    def __init__(self, val):
        self.val = val
        self.next = None


class Linklist:
    def __init__(self, f_pointer=None, l_pointer=None, l=0):
        self.first = f_pointer
        self.last = l_pointer
        self.len = l

    def print(self):
        p = self.first
        print('[', end='')
        while p is not None:
            print(p.val, end=', ' if p.next is not None else '')
            p = p.next
        print(']')

    def append(self, val):
        q = Node(val)
        if self.first is not None:
            self.last.next = q
        else:
            self.first = q
        self.last = q
        self.len += 1

    def extend(self, *vals):
        for val in vals:
            self.append(val)

    def reverse(self):
        q = None
        p = self.first
        while p is not None:
            t = p.next
            p.next = q
            q = p
            p = t
        self.first = q
    
    def into_ten(self):
        first_pointer = [None for _ in range(10)]
        last_pointer = [None for _ in range(10)]
        p = self.first
        while p is not None:
            digit = p.val % 10
            if first_pointer[digit] is None:
                first_pointer[digit] = p
                last_pointer[digit] = p
            else:
                last_pointer[digit].next = p
                last_pointer[digit] = p
            t = p
            p = p.next
            t.next = None
        s = None
        for i in range(10):
            if s is None and first_pointer[i] is not None:
                s = first_pointer[i]
                t = last_pointer[i]
            elif first_pointer[i] is not None:
                t.next = first_pointer[i]
                t = last_pointer[i]
        self.first = s
        self.last = t




def merge_linklists(l_1, l_2):
    p_1 = l_1.first
    p_2 = l_2.first
    if p_1 is None:
        return l_2
    if p_2 is None:
        return l_1
    
    if p_1.val < p_2.val:
        s = p_1
        p_1 = p_1.next
    else:
        s = p_2
        p_2 = p_2.next
    
    p = s

    while p_1 is not None and p_2 is not None:
        if p_1.val < p_2.val:
            p.next = p_1
            p_1 = p_1.next
        else:
            p.next = p_2
            p_2 = p_2.next
        p = p.next
    
    if p_1 is None and p_2 is None: # nigdy się nie zdarzy (?)
        l = Linklist(s, p, l_1.len+l_2.len)
    if p_1 is None:
        p.next = p_2
        l = Linklist(s, l_2.last, l_1.len+l_2.len)
    if p_2 is None:
        p.next = p_1
        l = Linklist(s, l_1.last, l_1.len+l_2.len)
    return l


if __name__ == '__main__':
    l = Linklist()
    tmp = [randint(1000, 9999) for _ in range(15)]
    l.extend(*tmp)
    l.print()
    # l.reverse()
    # l.print()

    l.into_ten()
    l.print()

    # l2 = Linklist()
    # tmp = sorted([randint(0, 9) for _ in range(1)])
    # l2.extend(*tmp)
    # l2.print()
    # lll = merge_linklists(l, l2)
    # lll.print()


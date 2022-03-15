import heapsort as hps


class Vertex():
    def __init__(self, no):
        self.no = no
        self.edges = []
        # self.path_via = None
        self.path_cost = 10**100
        self.done = False
        self.in_heap = False


class Edge():
    def __init__(self, cost, src):
        self.cost = cost
        self.src = src
        self.dst = None


def parser():
    a = input()
    data = []
    while a:
        data_row = []
        for ch in a:
            data_row.append(int(ch))
        data.append(data_row)
        a = input()
    return data


def map_extender(tab):
    n = len(tab)
    new_tab = [[0 for _ in range(n*5)] for _ in range(n*5)]
    for i in range(n):
        for j in range(n):
            t = tab[i][j]
            ot = t
            for x in range(5):
                for y in range(5):
                    new_tab[x*n+i][y*n+j] = t
                    t += 1
                    if t == 10:
                        t = 1
                ot += 1
                if ot == 10:
                    ot = 1
                t = ot
    return new_tab


def d15(tab):
    n = len(tab)
    pointers = [[Vertex(i*n+j) for j in range(n)] for i in range(n)]

    for i in range(n*n):
        r = i//n
        c = i % n
        v = pointers[r][c]
        e_up = Edge(tab[r-1][c], v) if r > 0 else None
        e_left = Edge(tab[r][c-1], v) if c > 0 else None
        e_down = Edge(tab[r+1][c], v) if r < n-1 else None
        e_right = Edge(tab[r][c+1], v) if c < n-1 else None

        if e_up:
            t = pointers[r-1][c]
            e_up.dst = t
            v.edges.append(e_up)
        if e_left:
            t = pointers[r][c-1]
            e_left.dst = t
            v.edges.append(e_left)
        if e_down:
            t = pointers[r+1][c]
            e_down.dst = t
            v.edges.append(e_down)
        if e_right:
            t = pointers[r][c+1]
            e_right.dst = t
            v.edges.append(e_right)

    s = pointers[0][0]
    s.path_cost = 0
    s.in_heap = True
    heap = [[s.path_cost, s]]
    while True:
        _, v = hps.heap_extract(heap, True, True, 0)
        if v.no == n*n-1:
            return v.path_cost

        for edge in v.edges:
            t = edge.dst
            if not t.done:
                new_cost = edge.cost + v.path_cost
                if new_cost < t.path_cost:
                    t.path_cost = new_cost
                    # t.path_via = v
                if not t.in_heap:
                    hps.heap_insert(heap, [t.path_cost, t], True, True, 0)
                    t.in_heap = True

        v.done = True


if __name__ == '__main__':
    tab = parser()
    tab = map_extender(tab)
    print(d15(tab))

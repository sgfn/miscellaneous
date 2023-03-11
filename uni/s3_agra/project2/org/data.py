from org.testy import *


def lcg(seed):
    a = 1103515245
    a = 69069
    c = 12345
    m = 2 ** 31
    while True:
        yield seed ^ (seed >> 16)
        seed = (a * seed + c) % m

generator = lcg(314159265)
myrand = lambda a, b: a + next(generator) % (b - a + 1)

def myrand_shuffle(xs):
    n = len(xs)
    for i in range(n - 1, 0, -1):
        j = myrand(0, i)
        tmp = xs[i]
        xs[i] = xs[j]
        xs[j] = tmp

def permute(N, edges):
    vs = list(range(1, N + 1))
    myrand_shuffle(vs)
    return [(vs[i-1], vs[j-1]) for i, j in edges]


def make_clique(N):
    return [N, [(i, j) for i in range(1, N+1) for j in range(i + 1, N + 1)]]

def make_sparse(N, conn):
    def flip(): return myrand(0, 1000) / 1000.0 < conn
    return [N, [(i, j) for i in range(1, N+1) for j in range(i + 1, N + 1) if flip()]]

def make_random_solvable(N, k, conn):
    def flip(): return myrand(0, 1000) / 1000.0 < conn
    _, core = make_clique(k)
    other = [(i, j) for i in range(1, k + 1) for j in range(k + 1, N + 1) if flip()]
    edges = permute(N, core + other)
    myrand_shuffle(edges)
    return [N, edges]


problems = [
    # Proste, zdegenerowane przypadki
    {"arg": [2, [(1,2)]], "hint": 1},
    {"arg": [3, [(1,2), (2,3)]], "hint": 1},
    {"arg": [3, [(1,2), (2,3), (3,1)]], "hint": 2},
    {"arg": [5, []], "hint": 1},
    {"arg": make_clique(5), "hint": 4},
    # Przykłady bez rozwiązania
    {"arg": [4, [(1,2), (2,3), (3,4), (4,1)]], "hint": None},
    {"arg": [5, [(1,2), (2,3), (3,4), (4,5), (5,1)]], "hint": None},
    {"arg": [6, [(1,2), (2,3), (4,5), (5,6), (2,6), (3,5), (3,6)]], "hint": None},
    # Przykład z opisu zadania
    {"arg": [10, [
        (1,2), (1, 3), (1, 4), (1, 5),
        (2, 3), (2, 4), (2, 5),
        (3, 4), (3, 5),
        (4, 5),
        (6, 1), (6, 2), (6, 5),
        (7, 2),
        (8, 2), (8, 3),
        (9, 4),
        (10, 2), (10, 3)
        ]],
    "hint": 5
    },
    # Większe przykłady
    {"arg": make_clique(1000), "hint": 999},
    {"arg": make_clique(2000), "hint": 1999},
    {"arg": make_sparse(200, 0.3), "hint": None},
    {"arg": make_sparse(200, 0.8), "hint": None},
    {"arg": make_sparse(200, 0.9), "hint": None},
    {"arg": make_random_solvable(2000, 200, 0.3), "hint": 200},
    {"arg": make_random_solvable(2000, 1000, 0.6), "hint": 1000},
    {"arg": make_random_solvable(10000, 100, 0.2), "hint": 100},
    {"arg": make_random_solvable(2000, 1900, 0.01), "hint": 1899},
]

def printarg(N, channels):
    print(f"{N} szpiegów, {len(channels)} kanałów")
    print(f"Kanały: {limit(channels, 120)}")

def printhint(hint):
    print("Wynik: {}".format(hint))

def printsol(sol):
    print("Uzyskany wynik: {}".format(sol))

def check(N, channels, hint, sol):
    if hint == sol:
        print("Test zaliczony")
        return True
    else:
        print("NIEZALICZONY!")
        return False

def runtests(f):
    internal_runtests(printarg, printhint, printsol, check, problems, f)

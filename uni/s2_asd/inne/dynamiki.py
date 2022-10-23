# ALGORYTMY DYNAMICZNE

class Node:
    def __init__(self, val) -> None:
        self.val = val
        self.vassals = []
        self.f = -1
        self.g = -1


def lis_solution(A, detailed=False):
    n = len(A)
    maxi = 0
    F = [1 for _ in A]
    if detailed:    history = [-1 for _ in A]

    for i in range(1, n):
        for j in range(0, i):
            if A[i] > A[j] and F[j]+1 > F[i]:
                F[i] = F[j]+1
                if detailed:    history[i] = j
        if F[i] > F[maxi]:      maxi = i

    if detailed:
        t = maxi
        path = []
        while t != -1:
            path.append(A[t])
            t = history[t]
        print(*path[::-1], sep=' ')

    return F[maxi]


def entree(dict, enlist=False):
    p_list = []
    for key, val in dict.items():
        p = Node(key[1])
        p.vassals = entree(val, enlist=True)
        p_list.append(p)
    return p_list if enlist else p_list[0]


def printree(proot, indent=0):
    print(f"{'    '*indent}{proot.val}: {{", end='')
    if len(proot.vassals) == 0:
        print('}')
        return
    else: print()

    for vassal in proot.vassals:
        printree(vassal, indent+1)
    print(f"{'    '*indent}}}")


def best_binge(king, detailed=False):
    def f(node):
        if node.f != -1:    return node.f
        node.f = node.val
        for vassal in node.vassals:
            node.f += g(vassal)
        node.f = max(node.f, g(node))
        return node.f
    
    def g(node):
        if node.g != -1:    return node.g
        node.g = 0
        for vassal in node.vassals:
            node.g += f(vassal)
        return node.g

    # def printem(node):    # INCORRECT
    #     if node.f != node.g:
    #         print(node.val, end=' ')
    #     for vassal in node.vassals:
    #         printem(vassal)

    f(king)
    # if detailed:
    #     printem(king)
    #     print()
    return king.f


def knapsack(W, P, B, detailed=False):
    if detailed:    F = [[0 for _ in range(B+1)] for _ in W]
    else:           F = [0 for _ in range(B+1)]
    n = len(W)
    
    for b in range(W[0], B+1):
        if detailed:    F[0][b] = P[0]
        else:           F[b] = P[0]
    
    for i in range(1, n):
        for b in range(B, -1, -1):
            if detailed:
                val = F[i-1][b-W[i]] + P[i] if b >= W[i] else 0
                F[i][b] = max( F[i-1][b], val )
            else:
                val = F[b-W[i]] + P[i] if b >= W[i] else 0
                F[b] = max( F[b], val )

    if detailed:
        i = n-1
        b = B
        while i > 0:
            if F[i-1][b] != F[i][b]:
                print(f'{P[i]} zł/{W[i]} kg')
                b -= W[i]
            i -= 1
        if b > W[0]:    print(f'{P[0]} zł/{W[0]} kg')

    return F[n-1][B] if detailed else F[B]


def substring_sum(T, N, detailed=False):
    el_amnt = len(T)
    if detailed:
        F = [[False for _ in range(N+1)] for _ in T]
        F[0][0] = True
        if T[0] <= N:   F[0][T[0]] = True
    else:
        F = [False for _ in range(N+1)]
        F[0] = True

    for i in range(1, el_amnt):
        if detailed:
            for n in range(N+1):
                if   F[i-1][n]:                         F[i][n] = True
                elif n-T[i] >= 0 and F[i-1][n-T[i]]:    F[i][n] = True
        else:
            for n in range(N, -1, -1):
                if n-T[i] >= 0 and F[n-T[i]]:   F[n] = True

    if detailed:
        i = el_amnt - 1
        n = N
        while i > 0:
            if F[i-1][n] != F[i][n]:
                print(T[i], end=' ')
                n -= T[i]
            i -= 1
        if n == T[0]:   print(T[0])
        else:           print()

    return F[el_amnt-1][N] if detailed else F[N]


def matrix_multiplication(T, detailed=False):
    N = len(T)-1
    F = [[0 for _ in range(N)] for _ in range(N)]
    if detailed:    mem = [[-1 for _ in range(N)] for _ in range(N)]
    for first in range(1, N):
        i = 0
        while first + i < N:
            j = first+i
            res = (float)('inf')
            m = -1
            for k in range(i, j):
                cost = F[i][k] + F[k+1][j] + T[i]*T[k+1]*T[j+1]
                if cost < res:
                    res = cost
                    m = k-i
            F[i][j] = res
            if detailed:    mem[i][j] = m
            i += 1
    
    if detailed: # unfinished
        i = 0
        j = N-1
        m = mem[i][j]
        while m != -1:
            pass
    return F[0][N-1]


def denominations(N, K, detailed=False):
    F = [(float)('inf') for _ in range(K+1)]

    F[0] = 0
    for n in N:
        for k in range(n, K+1):
            F[k] = min( F[k], F[k-n]+1 )
    
    return F[K]


if __name__ == '__main__':
    # A = [2, 1, 4, 3, 4, 8, 5, 7, 2, 0]
    # print(lis_solution(A, detailed=True))

    # d = {(0, 50): {(0, 10): {(0, 17): {}, (1, 0): {(0, 0): {}, (1, 0): { (0, 0): {},
    #      (1, 0): {}, (2, 0): {}}}, (2, 25): {}}, (1, 25): {}, (2, 40): { (0, 5): {
    #      (0, 6): {}, (1, 17): {}}, (1, 20): {}, (2, 15): {(0, 500): {(0, 10): {
    #      (0, 100): {}}}, (1, 20): {}}, (3, 10): {}}}}
    # king = entree(d)
    # printree(king)
    # print(best_binge(king, detailed=True))

    # W = [5, 2, 3, 10]
    # P = [500, 15, 100, 60]
    # B = 15
    # print(knapsack(W, P, B, detailed=True))

    # T = [5, 10, 2, 3, 1, 2, 7, 20, 33, 1, 11, 15]
    # print(substring_sum(T, 115, detailed=True))

    T = [2, 3, 1, 7]
    print(matrix_multiplication(T))

    # N = [3, 4, 2, 7]
    # print(denominations(N, 14))

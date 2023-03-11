from heapq import heapify as k, heappop as l, heappush as m

from data import runtests


def my_solve(N, M, K, base, wages, eq_cost): # O((K+N) log N + NM log M) maybe idk
    a = [sorted((h+eq_cost[g-1] for g, h in i)) for i in wages] # O(NM log M)
    b = [0 for _ in range(N)] # O(N)
    c = [(a[j][0] + base[j][0], j) for j in range(N)] # O(N)
    d = 0
    k(c) # O(N log N)
    for _ in range(K): # O(K log N)
        e, f = l(c) # O(log N)
        b[f] += 1
        d += e
        if b[f] < len(a[f]) and b[f] < len(base[f]): m(c, (a[f][b[f]] + base[f][b[f]]-base[f][b[f]-1], f)) # O(log N)
    return d

runtests(my_solve)

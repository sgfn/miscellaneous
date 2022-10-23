"""
Jakub Pisarek

Rozwiązanie polega na obliczeniu długości wszystkich możliwych krawędzi
(autostrad) między wierzchołkami (miastami), zapakowaniu ich do listy i posorto-
waniu tejże. Następnie tworzony jest syntetyczny graf G (początkowo bez kra-
wędzi), który z założenia reprezentuje aktualnie badany stan mapy połączeń.
Po posortowanej liście idziemy od początku, dołączając krawędzie po kolei od
najkrótszej. Po każdym dołączeniu badamy spójność grafu G algorytmem BFS - gdy
stanie się spójny, zapamiętujemy aktualny wynik - różnicę między najdłuższą
a najkrótszą krawędzią - i zaczynamy odłączać krawędzie od najkrótszej począ-
wszy, za każdym razem badając spójność, licząc i ewentualnie aktualizując wynik.
Gdy graf ponownie przestanie być spójny, zaczynamy dodawać krawędzie, etc. etc.,
aż sprawdzimy wszystkie możliwe kombinacje krawędzi, przy których wynik może być
najniższy - jest to trik z dwoma wskaźnikami, więc działa w czasie liniowym.
Dodatkowo przeprowadzana jest mikrooptymalizacja - gdy usuwamy z grafu jakąś
krawędź, BFS rozpoczynamy z jednego z wierzchołków, które łączyła, co w części
przypadków pozwala szybciej wykryć jego niespójność.

Złożoność obliczeniowa rozwiązania na pewno wynosi O(n^4), być może mniej.
"""

from zad8testy import runtests

from collections import deque

def highway( A ):
    def is_connected(G, s):
        # using BFS, thus complexity: O(V+E)
        Q = deque()
        visited = [False for _ in G]
        visited[s] = True
        vis_amount = 1
        Q.append(s)
        while Q:
            u = Q.popleft()
            for v in G[u]:
                if not visited[v]:
                    visited[v] = True
                    vis_amount += 1
                    Q.append(v)
        return vis_amount == len(G)

    d = lambda p_1, p_2: ( (p_1[0]-p_2[0])**2 + (p_1[1]-p_2[1])**2 ) ** 0.5
    ceil = lambda x: int(x) if int(x) == x else int(x)+1

    N = len(A)
    if N == 1:      return 0
    dists = []
    for j in range(1, N): # O(n^2)
        for i in range(j):
            dists.append(( ceil( d(A[i], A[j]) ), i, j ))
    dists = sorted(dists) # O(n^2*log n)
    M = len(dists)

    G = [[] for _ in A]
    first, last = 0, -1
    bfs_from = 0
    res = (float)('inf')
    while last < M: # O(n^2*[BFS])
        if is_connected(G, bfs_from):
            res = min( res, dists[last][0] - dists[first][0] )
            _, u, v = dists[first]
            G[u].remove(v) # O(n), irrelevant due to the complexity of BFS
            G[v].remove(u)
            bfs_from = u
            first += 1
        else:
            if last < M-1:
                _, u, v = dists[last+1]
                G[u].append(v)
                G[v].append(u)
            last += 1
        
    return res

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( highway, all_tests = True )

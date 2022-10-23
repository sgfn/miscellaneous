"""
Jakub Pisarek

Rozwiązanie bazuje na algorytmie przeszukiwania grafu wszerz (BFS).
Na początek uruchamiamy BFS z wierzchołka s, zapamiętując dystans i rodzica
każdego odwiedzonego wierzchołka. Jeżeli algorytm po raz drugi znajdzie trasę
do jakiegoś wierzchołka (trasę tej samej długości), to dopisujemy następnego
rodzica do listy rodziców. Gdy nie udało się dotrzeć do wierzchołka t, zwracamy
None, w przeciwnym wypadku - możemy się cofać od wierzchołka t, patrząc po
wszystkich dostępnych rodzicach. Ponownie robimy coś na kształt BFS-a, w celu
sprawdzenia, czy kiedykolwiek mamy tylko jedną dostępną najkrótszą drogę powrotu
do s - idziemy po parentach wierzchołków, pakując ich kolejno do kolejki. Jeśli
kiedykolwiek w kolejce będziemy mieli tylko jeden wierzchołek - po usunięciu
następnej krawędzi najkrótsza trasa między s a t się wydłuży. Kończymy wykonanie
drugiego BFS gdy dotrzemy do s.

Złożoność obliczeniowa rozwiązania wynosi O(V+E).
"""

from zad6testy import runtests
from collections import deque

def longer( G, s, t ):
    Q = deque()
    visited = [False for _ in G]
    distance = [None for _ in G]
    parents = [[] for _ in G]

    distance[s] = 0
    visited[s] = True
    Q.append(s)

    while Q:
        u = Q.popleft()
        current_distance = distance[u] + 1
        for v in G[u]:
            if not visited[v]:
                visited[v] = True
                distance[v] = current_distance
                parents[v].append(u)
                Q.append(v)

            elif distance[v] == current_distance:
                parents[v].append(u)

    if not visited[t]:      return None

    visited = [False for _ in G]
    current_node = t
    while current_node != s:
        if not visited[current_node]:
            visited[current_node] = True
            Q.extend(parents[current_node])
        
        if len(Q) == 1:     return (current_node, parents[current_node][0])  

        current_node = Q.popleft()

    return None

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( longer, all_tests = True )

"""
Jakub Pisarek

Rozwiązanie bazuje na algorytmie wyszukiwania najkrótszych ścieżek Dijkstry.

Na początku graf przekształcam do postaci listy sąsiedztwa, dodając do niego
zarazem syntetyczny wierzchołek o indeksie n, który to jest reprezentacją
osobliwości z układu planetarnego (c)Algon - prowadzą do niego krawędzie
z wszystkich wierzchołków z S, każda o wadze 0.

Następnie na tak przekształconym grafie uruchamiam algorytm Dijkstry z wierz-
chołka a. Stosuję dodatkowo tablicę 'finished', w której trzymam aktualny stan
każdego wierzchołka: False - niezakolejkowany/w trakcie przetwarzania,
True - przetworzony (gdy wierzchołek został już przetworzony, nie rozważam go
ponownie, nawet jeśli pojawił się przez wyjęcie z kolejki priorytetowej ze
starą wartością odległości, przed relaksacją).

Wynik algorytmu znajduje się w tablicy odległości 'dists' pod indeksem b -
jeżeli wynosi INF, droga nie istnieje.

Złożoność obliczeniowa rozwiązania wynosi O(m log n).
"""

from queue import PriorityQueue as pq

from kol3atesty import runtests

def spacetravel( n, E, S, a, b ):
    INF = (float)('inf')
    PQ = pq()

    n += 1
    dist = [INF for _ in range(n)]
    finished = [False for _ in range(n)]

    # Represent graph as adjacency matrix
    G = [[] for _ in range(n)]
    for fr, to, d in E: # O(m)
        G[fr].append( (to, d) )
        G[to].append( (fr, d) )
    # Create a synthetic vertex 'connecting' vertices from S
    for hyper_to in S: # O(n)
        G[n-1].append( (hyper_to, 0) )
        G[hyper_to].append( (n-1, 0) )

    # DIJKSTRA - O(m log n)
    dist[a] = 0
    PQ.put( (dist[a], a) )
    while not PQ.empty():
        _, u = PQ.get()
        if not finished[u]:
            for v, d in G[u]:
                # DIJKSTRA RELAX
                if dist[v] > dist[u] + d:
                    dist[v] = dist[u] + d
                    PQ.put( (dist[v], v) )
            
            finished[u] = True

    return None if dist[b] == INF else dist[b]

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( spacetravel, all_tests = True )

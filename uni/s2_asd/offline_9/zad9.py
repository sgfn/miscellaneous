"""
Jakub Pisarek

Rozwiązanie to algorytm brute-force, obliczający maksymalny przepływ metodą
Forda-Fulkersona (z wykorzystaniem algorytmu Edmondsa-Karpa) dla każdej pary
wierzchołków niebędących wierzchołkiem startowym - i zwracający maksimum
z tychże wartości.

Przygotowanie do wykonania wyżej wymienionego algorytmu polega na stworzeniu 
drugiej reprezentacji grafu wejściowego (w postaci listy sąsiedztwa), używając
obiektów PipelineObj dla każdego odcinka rurociągu. Obiekty te zawierają nastę-
pujące informacje: do jakiego miasta prowadzi rurociąg, jaka jest jego przepu-
stowość, ile aktualnie przez niego płynie; jak również, wskaźnik do rurociągu
płynącego w przeciwną stronę, który okazuje się niezbędny (implementacja sieci
rezydualnej). Do grafu dołączamy również wierzchołek - uniwersalne ujście.

Złożoność obliczeniowa rozwiązania wynosi O( V^3 * E^2 ).
"""

from zad9testy import runtests
from collections import deque

def maxflow( G,s ):
    class PipelineObj:
        def __init__(self, to, cap) -> None:
            self.to = to
            self.cap = cap
            self.flow = 0
            self.rev = None

    n = 0
    for fr, to, _ in G:     n = max( n, max(fr, to) )
    n += 2      # last city - universal outlet

    l_G = [[] for _ in range(n)]
    for fr, to, cap in G:
        obj_1, obj_2 = PipelineObj(to, cap), PipelineObj(fr, 0)
        obj_1.rev = obj_2
        obj_2.rev = obj_1
        l_G[fr].append(obj_1)
        l_G[to].append(obj_2)

    uni_out_obj_1 = PipelineObj(n-1, (float)('inf'))
    uni_out_obj_2 = PipelineObj(n-1, (float)('inf'))
    dummy = PipelineObj(-9001, -9001) # necessary for flow updater not to break
    uni_out_obj_1.rev = dummy
    uni_out_obj_2.rev = dummy

    max_flow = 0
    for c_1 in range(n-1):
        if c_1 == s:    continue
        l_G[c_1].append(uni_out_obj_1) # set universal outlets
        for c_2 in range(c_1+1, n-1):
            if c_2 == s:    continue
            l_G[c_2].append(uni_out_obj_2)

            curr_flow = 0
            min_f = 9001
            while min_f > 0:
                # BFS
                Q = deque()
                parent = [None for _ in l_G]
                Q.append(s)
                while Q:
                    u = Q.popleft()
                    for i, obj in enumerate( l_G[u] ):
                        v = obj.to
                        if obj.cap > obj.flow:
                            if parent[v] is None and v != s:
                                parent[v] = (u, i)
                                Q.append(v)

                # calculate min flow of found path (if there is one)
                min_f = (float)('inf')
                curr = n-1
                while parent[curr] is not None:
                    obj = l_G[ parent[curr][0] ][ parent[curr][1] ]
                    min_f = min( min_f,  obj.cap - obj.flow )
                    curr = parent[curr][0]
                
                if min_f == (float)('inf'):     min_f = 0
                else:   # update flows
                    curr = n-1
                    while parent[curr] is not None:
                        obj = l_G[ parent[curr][0] ][ parent[curr][1] ]
                        obj.flow += min_f
                        obj.rev.flow -= min_f
                        curr = parent[curr][0]

                curr_flow += min_f
            max_flow = max( max_flow, curr_flow )

            # clean up
            for obj_list in l_G:
                for obj in obj_list:        obj.flow = 0
            l_G[c_2].pop()
        l_G[c_1].pop()

    return max_flow

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( maxflow, all_tests = True )

from collections import deque
from queue import PriorityQueue

import testing


def sol_sw(V, edge_list):
    G = [{} for _ in range(V)]
    for (x, y, c) in edge_list:
        G[x-1][y-1] = c
        G[y-1][x-1] = c

    res = (float)('inf')
    for vcs in range(V, 1, -1):
        # min-cut phase
        a = 0
        S = {a}
        consider = [True for _ in G]
        wt_sum = [v_edges.get(a, 0) for v_edges in G]
        pq = PriorityQueue()
        m_2, m_1 = a, None
        for v in range(V):
            if v != a:
                pq.put((-wt_sum[v], v))

        while len(S) != vcs:
            _, v = pq.get()
            if not consider[v]:
                continue
            consider[v] = False
            for to, wt in G[v].items():
                if to in S:
                    continue
                if consider[to]:
                    wt_sum[to] += wt
                    pq.put((-wt_sum[to], to))
            S.add(v)
            m_1 = m_2
            m_2 = v
        res = min(res, sum(G[m_2].values()))

        # merge vertices
        for to, wt in G[m_1].items():
            if to != m_2:
                G[m_2][to] = G[m_2].get(to, 0) + wt
                G[to][m_2] = G[to].get(m_2, 0) + wt
                G[to].pop(m_1, 0)
        G[m_2].pop(m_1, 0)

    return res


def sol_ff(V, edge_list):
    class PipelineObj:
        def __init__(self, to, cap) -> None:
            self.to = to
            self.cap = cap
            self.flow = 0
            self.rev = None


    l_G = [[] for _ in range(V)]
    for fr, to, _ in edge_list:
        obj_1, obj_2 = PipelineObj(to-1, 1), PipelineObj(fr-1, 1)
        obj_1.rev = obj_2
        obj_2.rev = obj_1
        l_G[fr-1].append(obj_1)
        l_G[to-1].append(obj_2)

    global_min_max_flow = 9001
    s = 0
    for t in range(1, V):
        max_flow = 0
        min_f = 9001
        while min_f > 0:
            # use BFS to find path
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
            curr = t
            while parent[curr] is not None:
                obj = l_G[ parent[curr][0] ][ parent[curr][1] ]
                min_f = min( min_f,  obj.cap - obj.flow )
                curr = parent[curr][0]
            
            if min_f == (float)('inf'):
                min_f = 0
            else:   # update flows
                curr = t
                while parent[curr] is not None:
                    obj = l_G[ parent[curr][0] ][ parent[curr][1] ]
                    obj.flow += min_f
                    obj.rev.flow -= min_f
                    curr = parent[curr][0]

            max_flow += min_f

        global_min_max_flow = min(global_min_max_flow, max_flow)
        # cleanup
        for obj_list in l_G:
            for obj in obj_list:
                obj.flow = 0

    return global_min_max_flow


def main():
    testing.test_from_dir('connectivity/', sol_ff, sol_sw, more_paths=('connectivity2/',), time_limit=5)


if __name__ == '__main__':
    main()

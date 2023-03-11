from collections import deque

import testing


def get_parents_bfs(l_G, s):
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
    return parent


def get_parents_dfs(l_G, s):
    def dfs_visit(u):
        visited[u] = True
        for i, obj in enumerate( l_G[u] ):
            v = obj.to
            if obj.cap > obj.flow:
                if not visited[v]:
                    parent[v] = (u, i)
                    dfs_visit(v)

    visited = [False for _ in l_G]
    parent = [None for _ in l_G]
    dfs_visit(s)
    return parent


def sol_general(V, edge_list, get_parents_fun):
    class PipelineObj:
        def __init__(self, to, cap) -> None:
            self.to = to
            self.cap = cap
            self.flow = 0
            self.rev = None


    s, t = 0, V-1
    l_G = [[] for _ in range(V)]
    for fr, to, cap in edge_list:
        obj_1, obj_2 = PipelineObj(to-1, cap), PipelineObj(fr-1, 0)
        obj_1.rev = obj_2
        obj_2.rev = obj_1
        l_G[fr-1].append(obj_1)
        l_G[to-1].append(obj_2)

    max_flow = 0
    min_f = 9001
    while min_f > 0:
        # use either BFS or DFS to find path
        parent = get_parents_fun(l_G, s)

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

    return max_flow


def sol_bfs(V, edge_list):
    return sol_general(V, edge_list, get_parents_bfs)


def sol_dfs(V, edge_list):
    return sol_general(V, edge_list, get_parents_dfs)


def main():
    testing.test_from_dir('flow/', sol_dfs, sol_bfs, directed=True, time_limit=10)


if __name__ == '__main__':
    main()

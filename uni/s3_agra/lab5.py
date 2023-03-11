import testing


def checkLexBFS(G, vs):
    n = len(G)
    pi = [None] * n
    for i, v in enumerate(vs):
        pi[v] = i

    for i in range(n-1):
        for j in range(i+1, n-1):
            Ni = G[vs[i]]
            Nj = G[vs[j]]

            verts = [pi[v] for v in Nj - Ni if pi[v] < i]
            if verts:
                viable = [pi[v] for v in Ni - Nj]
                if not viable or min(verts) <= min(viable):
                    return False
    return True


def loadgraph(V, edge_list):
    l_G = [set() for _ in range(V)]
    for fr, to, _ in edge_list:
        l_G[fr-1].add(to-1)
        l_G[to-1].add(fr-1)
    return l_G


def lexbfs(G):
    V = len(G)
    order = []
    notvisited = [set((i for i in range(1, V))), {0}]
    while notvisited:
        s = notvisited[-1].pop()
        newnotvisited = []
        for X in notvisited:
            K = X - G[s]
            Y = X & G[s]
            for ns in K, Y:
                if len(ns) > 0:
                    newnotvisited.append(ns)
        order.append(s)
        notvisited = newnotvisited

    return order


def sol_chordal(V, edge_list):
    l_G = loadgraph(V, edge_list)
    order = lexbfs(l_G)

    # isPEO
    previous_vertices = {order[0]}
    for i in range(1, V):
        v = order[i]
        RNv = previous_vertices & l_G[v]
        ppind = None
        for j in range(i, -1, -1):
            if order[j] in RNv:
                ppind = j
                break
        if ppind is None:
            print('fd')
            return False

        if not RNv - {order[ppind]} <= set((f for f in order[:ppind])) & l_G[order[ppind]]:
            return False
        previous_vertices.add(v)
    return True


def sol_maxclique(V, edge_list):
    l_G = loadgraph(V, edge_list)
    order = lexbfs(l_G)

    # find max clique
    result = -1
    previous_vertices = {order[0]}
    for i in range(1, V):
        v = order[i]
        RNv = previous_vertices & l_G[v]
        result = max(result, len(RNv)+1)
        previous_vertices.add(v)

    return result


def sol_colouring(V, edge_list):
    l_G = loadgraph(V, edge_list)
    order = lexbfs(l_G)

    colour = [0 for _ in range(V)]
    available_colours = {1}
    for v in order:
        used = {colour[u] for u in l_G[v]}
        c = min(available_colours - used)
        if c == len(available_colours):
            available_colours.add(c+1)
        colour[v] = c

    return max(colour)


def sol_vcover(V, edge_list):
    l_G = loadgraph(V, edge_list)
    order = lexbfs(l_G)

    I = set()
    for v in order[::-1]:
        if not I & l_G[v]:
            I.add(v)

    return V-len(I)


def main():
    testing.test_from_dir('chordal/', sol_chordal)
    testing.test_from_dir('maxclique/', sol_maxclique)
    testing.test_from_dir('colouring/', sol_colouring)
    testing.test_from_dir('vcover/', sol_vcover)

if __name__ == '__main__':
    main()

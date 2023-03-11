from collections import deque

from data import runtests


def my_solve(N, channels):
    class lln:
        def __init__(self, data):
            self.data = data
            self.next = None
            self.prev = None

    G = [set() for _ in range(N)]
    for fr, to in channels:
        G[fr-1].add(to-1)
        G[to-1].add(fr-1)

    # lexbfs
    order = []
    nvfirst = lln(set(range(N)))
    set_map = [nvfirst for _ in range(N)]

    usable_llns = deque()

    rechecked = set()
    while nvfirst is not None:
        node = nvfirst
        v = node.data.pop()
        set_map[v] = None

        if len(node.data) == 0:
            nvfirst = node.next
            if nvfirst is not None: nvfirst.prev = None
            usable_llns.append(node)

        rechecked.clear()

        order.append(v)
        for w in G[v]:
            node = set_map[w]
            if node is not None:
                if node not in rechecked:
                    if len(usable_llns) > 0:
                        prior = usable_llns.pop()
                        prior.prev = None
                        prior.next = None
                    else:
                        prior = lln(set())

                    if node.prev is not None:
                        node.prev.next = prior
                        prior.prev = node.prev
                    else:
                        nvfirst = prior
                    prior.next = node
                    node.prev = prior

                    rechecked.add(node)

                else:
                    prior = node.prev

                node.data.remove(w)
                prior.data.add(w)
                set_map[w] = prior

                if len(node.data) == 0:
                    if node == nvfirst: nvfirst = node.next
                    if node.next is not None: node.next.prev = node.prev
                    if node.prev is not None: node.prev.next = node.next
                    usable_llns.append(node)

    # maxclique
    maxclique = set()
    RNv = set()
    omap = {vi: oi for oi, vi in enumerate(order)}
    sscache = {}
    for i in range(1, N):
        v = order[i]
        pnt = -1
        RNv.clear()
        if len(G[v]) < i:
            for x in G[v]:
                if omap[x] < i:
                    RNv.add(x)
                    pnt = max(pnt, omap[x])
        else:
            for yoind in range(i):
                if order[yoind] in G[v]:
                    RNv.add(order[yoind])
                    pnt = max(pnt, yoind)

        # ispeo
        if pnt != -1:
            if pnt not in sscache: sscache[pnt] = {f for f in order[:pnt]} & G[order[pnt]]
            for rnvx in RNv:
                if rnvx != order[pnt] and rnvx not in sscache[pnt]: return None

        if len(maxclique) < len(RNv)+1:
            if order[pnt] not in maxclique:
                maxclique = RNv.copy()
            maxclique.add(v)

    # check n-1
    consider = list(maxclique) + [None]
    for xv in consider:
        ok = True
        for v in range(N):
            if v == xv: pass
            elif v in maxclique: continue

            for nv in G[v]:
                if nv == xv or nv not in maxclique:
                    ok = False
                    break

            if not ok: break
        if ok: return max(len(maxclique) - (1-(xv is None)), 1)

    return None

runtests(my_solve)

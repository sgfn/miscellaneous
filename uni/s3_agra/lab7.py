import networkx as nx

import testing


def sol_planar(V, edge_list):
    G = nx.Graph()
    G.add_nodes_from((i for i in range(V)))
    for fr, to, _ in edge_list:
        G.add_edge(fr-1, to-1)
    return nx.algorithms.check_planarity(G)[0]


def sol_flow(V, edge_list):
    G = nx.DiGraph()
    G.add_nodes_from((i for i in range(V)))
    for fr, to, wt in edge_list:
        G.add_edge(fr-1, to-1)
        G[fr-1][to-1]['capacity'] = wt
    return nx.algorithms.flow.maximum_flow(G, 0, V-1)[0]


def sol_sat(V, cnf_formula):
    def check_solution(values):
        for ora, orb in cnf_formula:
            val = False
            for orx in ora, orb:
                if orx < 0:
                    val |= not values[-orx-1]
                else:
                    val |= values[orx-1]

            if not val:
                print("SOLUTION INCORRECT")
                return
        print("Solution OK")


    G = nx.DiGraph()
    G.add_nodes_from((i for i in range(1, V+1)))
    G.add_nodes_from((-i for i in range(1, V+1)))
    for ora, orb in cnf_formula:
        G.add_edge(-ora, orb)
        G.add_edge(-orb, ora)

    SCCGEN = nx.algorithms.components.strongly_connected_components(G)
    SCC = [s for s in SCCGEN]
    
    H = nx.DiGraph()
    for i, S in enumerate(SCC):
        H.add_node(i)
        for v in S:
            if -v in S: return False
            for j, OS in enumerate(SCC):
                if i == j: continue
                for ov in OS:
                    if ov in G[v]:
                        H.add_edge(i, j)

    values = [None for _ in range(V)]
    O = nx.algorithms.topological_sort(H)
    for s in O:
        for x in SCC[s]:
            if x < 0:
                if values[-x-1] is None:
                    values[-x-1] = True
            else:
                if values[x-1] is None:
                    values[x-1] = False

    check_solution(values)
    return True


def main():
    testing.test_from_dir('graphs-lab7/', sol_planar)
    testing.test_from_dir('flow/', sol_flow, directed=True)
    testing.test_from_dir('sat/', sol_sat, cnf=True)

if __name__ == '__main__':
    main()

import testing

class FindUnion:
    def __init__(self, elems) -> None:
        self.leader = [None for _ in range(elems)]

    def makeset(self, x):
        self.leader[x] = x

    def find(self, x):
        if self.leader[x] is None:
            return None
        if x != self.leader[x]:
            self.leader[x] = self.find(self.leader[x])
        return self.leader[x]

    def union(self, x, y):
        x = self.find(x)
        y = self.find(y)
        if x == y: return

        self.leader[x] = y

    def print(self):
        print(*self.leader)


def sol_find_union(V, edge_list):
    fu = FindUnion(V)
    fu.makeset(0)
    fu.makeset(1)
    for fr, to, wt in sorted(edge_list, key=lambda x: -x[2]):
        if fu.find(fr-1) is None: fu.makeset(fr-1)
        if fu.find(to-1) is None: fu.makeset(to-1)

        fu.union(fr-1, to-1)
        if fu.find(0) == fu.find(1):
            return wt

    return None


def sol_binsearch_dfs(V, edge_list):
    adjacency_list = [[] for _ in range(V)]
    for fr, to, wt in edge_list:
        adjacency_list[fr-1].append((to-1, wt))
        adjacency_list[to-1].append((fr-1, wt))

    raise NotImplementedError()


def main():
    testing.test_from_dir('graphs/', sol_find_union)


if __name__ == '__main__':
    main()

class Node():
    def __init__(self, name, type):
        self.name = name
        self.type = type
        self.connects_to = []


def recursive(dict, ans, node, mode=1, path=[], same_cave_flag = False):
    if mode == 2:
        if node in path:
            if dict[node].type in ('start', 'end'):
                return
            elif dict[node].type == 'small':
                if same_cave_flag:
                    return
                same_cave_flag = True
    else:
        if node in path and dict[node].type != 'big':
            return

    path.append(dict[node].name)
    if node == 'end':
        ans.append(path)
        return
    
    for connection in dict[node].connects_to:
        recursive(dict, ans, connection, mode, path.copy(), same_cave_flag)
    
    return


def pathgen(dict, mode=1):
    ans = []
    recursive(dict, ans, 'start', mode)
    return ans


def d12(data):
    storage = {}
    for con in data:
        for nd in con:
            if nd not in storage:
                if nd == 'start' or nd == 'end':
                    tp = nd
                elif nd.lower() == nd:
                    tp = 'small'
                else:
                    tp = 'big'
                storage[nd] = Node(nd, tp)

        nd_1, nd_2 = con
        storage[nd_1].connects_to.append(nd_2)
        storage[nd_2].connects_to.append(nd_1)

    # for ndobj in storage.values():
    #     print(ndobj.name, ndobj.type, ndobj.connects_to)
    
    # print(len(pathgen(storage)))
    print(len(pathgen(storage, mode=2)))
    
    
def parser():
    data = []
    a = input()
    while a:
        data.append(tuple(a.split('-')))
        a = input()
    return data


if __name__ == '__main__':
    data = parser()
    d12(data)
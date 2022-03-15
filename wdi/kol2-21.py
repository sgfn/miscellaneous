def recursive(t2):
    w = -1
    k = -1
    for i in range(201):
        for j in range(201):
            if t2[i][j] == 0:
                for b in range(j+1, 201):
                    if t2[i][b] == 0:
                        w = i
                        break
                if w != -1:
                    for c in range(j, 201):
                        if t2[w][c] == 0:
                            for a in range(i+1, 201):
                                if t2[a][c] == 0:
                                    k = c
                                    break
                        if k != -1:
                            break
                else:
                    k = j
                    for d in range(j+1, 201):
                        if t2[d][k] == 0:
                            for e in range(201):
                                if t2[d][e] == 0 and e != k:
                                    w = d
                                    break
                        if w != -1:
                            break
                
                if w == -1:
                    w = i
                if k == -1:
                    k = j

                flag = True
                for x in range(201):
                    for y in range(201):
                        if t2[x][y] < 2:
                            flag = False
                            break
                    if flag:
                        flag2 = True
                        # x to wiersz w którym są same dwójki
                        for p in range(201):
                            for q in range(201):
                                if t2[q][p] < 2:
                                    flag2 = False
                                    break
                            if flag2:
                                # możemy zabrać wieżę z pkt x,p i nic się nie stanie
                                return ((x, p), (w, k))
                        

def fun(t):
    t2 = [[0 for _ in range(201)] for _ in range(201)]
    n = 201 * 201
    for i in range(201):
        for j in range(201):
            if t[i][j]:
                for u in range(201):
                    t[u][j] += 1
                    t[i][u] += 1
                t[i][j] -= 1 # odejmujemy 1 gdy wieza szachuje wlasne pole a 2 jak nie
    return recursive(t2)
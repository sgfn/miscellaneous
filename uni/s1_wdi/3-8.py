def ex8(t):
    n = len(t)
    reachable = [False for _ in range(n)]
    reachable[0] = True
    for i in range(n):
        if reachable[i]:
            val = t[i]
            tmp = 2
            while val > 1:
                while val % tmp == 0:
                    val //= tmp
                    if i+tmp < n:
                        reachable[i+tmp] = True
                tmp += 1
    return reachable[n-1]

if __name__ == '__main__':
    t = [8, 4, 10, 3, 9, 1, 2]
    print(ex8(t))
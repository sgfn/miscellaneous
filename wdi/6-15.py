def change_val(tab, i, j, diff=1):
    for u in range(8):
        tab[u][j] += diff
        tab[i][u] += diff
    steps = ((1, 1), (-1, -1), (-1, 1), (1, -1))
    for a, b in steps:
        c, d=i, j
        while 0 <= c+a < 8 and 0 <= d+b < 8:
            c += a
            d += b
            tab[c][d] += diff


def recursive(tab, ans, i=0, j=0, H=1):
    ans[H-1]=[i, j]
    if H == 8:
        print(ans)
        exit()
    change_val(tab, i, j)
    for k in range(64):
        if tab[k//8][k%8] == 0:
            recursive(tab, ans, k//8, k%8, H+1)
    change_val(tab, i, j, -1)


def eight_queens():
    tab = [[0 for _ in range(8)] for _ in range(8)]
    ans = [[] for _ in range(8)]
    recursive(tab, ans)

if __name__ == '__main__':
    eight_queens()
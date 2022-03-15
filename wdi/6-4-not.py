def recursive(tab, r, c, val=1):
    n = len(tab)
    if 0 < tab[r][c] < val:
        return
    tab[r][c] = val
    
    for i in (1, 2):
        j = 2 // i
        for sgn_1 in (-1, 1):
            for sgn_2 in (-1, 1):
                if 0 <= r + sgn_1*i < n and 0 <= c + sgn_2*j < n:
                    recursive(tab, r + sgn_1*i, c + sgn_2*j, val+1)

def knightsmove(n=8, r=0, c=0):
    tab = [[0 for _ in range(n)] for _ in range(n)]
    recursive(tab, r, c)
    return tab

if __name__ == '__main__':
    ans = knightsmove(8)
    for row in ans:
        print(row)
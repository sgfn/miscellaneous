def get_available_moves(n):
    ans = [[0 for _ in range(n)] for _ in range(n)]
    if n == 3:
        ans = [[2, 2, 2], [2, 0, 2], [2, 2, 2]]
    elif n == 4:
        ans = [[2, 3, 3, 2], [3, 4, 4, 3], [3, 4, 4, 3], [2, 3, 3, 2]]
    if n < 5:
        return ans

    first, step_1, step_2 = 2, 1, 1
    for r in range(n//2 + 1):
        if r == 1:
            step_2 += 1
            first += 1
        elif r == 2:
            step_1 += 1
            first += 1
        t = first
        for c in range(n//2 + 1):
            if c == 1:
                t += step_1
            elif c == 2:
                t += step_2
            ans[r][c] = ans[n-r-1][c] = ans[r][n-c-1] = ans[n-r-1][n-c-1] = t
    return ans


def recursive(tab, mvs_tab, r, c, val=1, data=None):
    # Return values:
    # 0 - no errors, grid filled
    # 1 - unable to fill grid

    n = len(tab)
    tab[r][c] = val
    mvs_tab[r][c] = 0
    next_sq = [-1, -1, 9]
    for i in (1, 2):
        j = 2 // i
        for sgn_1 in (1, -1):
            for sgn_2 in (1, -1):
                next_r = r + sgn_1*i
                next_c = c + sgn_2*j
                if 0 <= next_r < n and 0 <= next_c < n:
                    mvs_tab[next_r][next_c] -= 1
                    if 0 < mvs_tab[next_r][next_c] < next_sq[2]:
                        next_sq = [next_r, next_c, mvs_tab[next_r][next_c]]
                    elif mvs_tab[next_r][next_c] == 0 and val+1 == n*n:
                        tab[next_r][next_c] = val+1
                        return 0
    if val+1 > n*n:
        return 0
    if next_sq[2] == 9:
        return 1
    return recursive(tab, mvs_tab, next_sq[0], next_sq[1], val+1)
    

def knight(n=8, r=0, c=0):
    tab = [[0 for _ in range(n)] for _ in range(n)]
    moves_tab = get_available_moves(n)
    exit_status = recursive(tab, moves_tab, r, c)
    # if exit_status:
    #     print(exit_status, n)
    return tab


if __name__ == '__main__':
    for i in range(5, 32):
        ans = knight(i)
        for row in ans:
            print(row)
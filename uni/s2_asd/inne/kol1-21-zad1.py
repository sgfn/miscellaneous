from random import randint

def Median(T):      # Time compl.: O(n^2), mem. compl.: O(1)
    n = len(T)

    f_med_indices = [(n*n-n)//2, (n*n+n)//2]
    f_med_vals = [None, None]
    
    for f_med_ind in range(2):
        ind = f_med_indices[f_med_ind]

        left, right = 0, n*n-1
        while True:
            # PARTITION
            i_sw = randint(left, right)
            T[right//n][right%n], T[i_sw//n][i_sw%n] = T[i_sw//n][i_sw%n], T[right//n][right%n]
            x = T[right//n][right%n]
            i = left - 1
            for j in range(left, right):
                if T[j//n][j%n] <= x:
                    i += 1
                    T[i//n][i%n], T[j//n][j%n] = T[j//n][j%n], T[i//n][i%n]
            T[(i+1)//n][(i+1)%n], T[right//n][right%n] = T[right//n][right%n], T[(i+1)//n][(i+1)%n]

            if i+1 == ind:
                f_med_vals[f_med_ind] = T[(i+1)//n][(i+1)%n]
                break
            elif i+1 < ind:
                left = i+1
            else:
                right = i+1

    # Fix the diagonal
    diag_i = 0
    for i in range(n):
        for j in range(n):
            if i == j:  continue
            if f_med_vals[0] <= T[i][j] < f_med_vals[1]:
                while f_med_vals[0] <= T[diag_i][diag_i] < f_med_vals[1]:
                    diag_i += 1
                T[i][j], T[diag_i][diag_i] = T[diag_i][diag_i], T[i][j]
                diag_i += 1
    
    # Swap values between upper and lower parts
    upper_i, upper_j = 0, 1
    lower_i, lower_j = 1, 0
    while True:
        while T[upper_i][upper_j] > f_med_vals[1]:
            upper_j += 1
            if upper_j == n:
                upper_i += 1
                upper_j = upper_i + 1
        if upper_i == n or upper_j == n:    break

        while T[lower_i][lower_j] < f_med_vals[0]:
            lower_i += 1
            if lower_i == n:
                lower_j += 1
                lower_i = lower_j + 1
        if lower_i == n or lower_j == n:    break

        T[upper_i][upper_j], T[lower_i][lower_j] = T[lower_i][lower_j], T[upper_i][upper_j]
        upper_j += 1
        if upper_j == n:
            upper_i += 1
            upper_j = upper_i + 1
        lower_i += 1
        if lower_i == n:
            lower_j += 1
            lower_i = lower_j + 1
        if upper_i == n or upper_j == n or lower_i == n or lower_j == n: break
            

    return T


if __name__ == '__main__':
    n = 5
    av = [i for i in range(1, 100)]
    t = [[] for _ in range(n)]
    for i in range(n):
        for _ in range(n):
            ind = randint(0, len(av)-1)
            t[i].append(av.pop(ind))

    print(*t, sep='\n')
    print()
    print(*Median(t), sep='\n')

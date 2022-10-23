def ex16(t):
    n = len(t)
    t_max = t[0]
    t_min = t[0]
    t_max_cnt = 1
    t_min_cnt = 1
    for i in range(1, n):
        if t[i] == t_max:
            t_max_cnt += 1
        if t[i] == t_min:
            t_min_cnt += 1
        elif t[i] > t_max:
            t_max = t[i]
            t_max_cnt = 1
        elif t[i] < t_min:
            t_min = t[i]
            t_min_cnt = 1
    if t_max_cnt == 1 and t_min_cnt == 1:
        return True
    else:
        return False

if __name__ == '__main__':
    print(ex16([1, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]))
def recursive(T, i=0, val_sum=0, ind_sum=0, subset_len=0):
    if subset_len > 0 and val_sum == ind_sum:
        return subset_len, val_sum
    if i == len(T):
        return 1e100, None
    a = recursive(T, i+1, val_sum+T[i], ind_sum+i, subset_len+1)
    b = recursive(T, i+1, val_sum, ind_sum, subset_len)
    return a if a[0] < b[0] else b

def ex6(T):
    ans = recursive(T)
    return ans[1]

if __name__ == '__main__':
    T = [1, 7, 3, 5, 11, 2]
    print(ex6(T))
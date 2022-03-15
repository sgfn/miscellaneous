from random import randint

def compute_cost(T, k, i=0, j=-1, val=0):
    if j == -1:
        j = k
    val += T[i][j]
    if i == 7:
        return val
    a = b = 1e100
    if j != 0:
        a = compute_cost(T, k, i+1, j-1, val)
    if j != 7:
        b = compute_cost(T, k, i+1, j+1, val)
    c = compute_cost(T, k, i+1, j, val)
    return min(a, b, c)


def compute_cost2(T, k, w=0):
    if w == 7:
        return T[w][k]
    a = b = 1e100
    if k != 0:
        a = compute_cost2(T, k-1, w+1)
    if k != 7:
        b = compute_cost2(T, k+1, w+1)
    c = compute_cost2(T, k, w+1)
    return min(a, b, c) + T[w][k]


if __name__ == '__main__':
    T = [[randint(1, 9) for _ in range(8)] for _ in range(8)]
    k = 7
    for row in T:
        print(row)
    print()
    print(compute_cost(T, k))
    print(compute_cost2(T, k))
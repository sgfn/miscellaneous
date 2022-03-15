from random import randint


def qs_k_lowest_values(tab, left, right, k):
    pivot_val = tab[(left+right)//2]
    i = left
    j = right

    while i <= j:
        while tab[i] < pivot_val:
            i += 1
        while tab[j] > pivot_val:
            j -= 1

        if i <= j:
            tab[i], tab[j] = tab[j], tab[i]
            i += 1
            j -= 1

    if j > k-1:
        qs_k_lowest_values(tab, left, j, k)
    else:
        if left < j:
            qs_k_lowest_values(tab, left, j, k)
        if i < right:
            qs_k_lowest_values(tab, i, right, k)


if __name__ == '__main__':
    tab = [randint(0, 999999) for _ in range(1000000)]
    qs_k_lowest_values(tab, 0, len(tab)-1, 50)
    print(tab[0:50])
    # tmp = max(tab[0:50])
    # for i in range(51, len(tab)):
    #     if tab[i] < tmp:
    #         print(f'value {tab[i]} at index {i} lower than {tmp}')

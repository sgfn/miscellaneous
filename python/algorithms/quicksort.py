from random import randint


def quicksort(tab, left, right):
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

    if left < j:
        quicksort(tab, left, j)
    if right > i:
        quicksort(tab, i, right)


def bubblesort(tab):
    for j in range(len(tab)-1, -1, -1):
        sorted_flag = True
        for i in range(0, j):
            if tab[i] > tab[i+1]:
                sorted_flag = False
                tab[i], tab[i+1] = tab[i+1], tab[i]
        if sorted_flag:
            return


if __name__ == '__main__':
    tab = [randint(100000, 999999) for _ in range(10000)]
    quicksort(tab, 0, len(tab)-1)
    # bubblesort(tab)

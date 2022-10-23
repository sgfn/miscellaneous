"""
Jakub Pisarek

Rozwiązanie sortuje tablicę T po początkach budynków (a), następnie dynamicznie
wylicza najlepszy możliwy zbiór budynków, zapamiętując odwołanie do poprzedniego
budynku ze zbioru (parent), sprawdzając przy tym, czy budynki ze sobą nie koli-
dują. Finalna wartość jest w ostatniej kolumnie tablicy F, wystarczy ją znaleźć
i odtworzyć drogę, jaką powstała, używając informacji o parentach z tablicy P.

Złożoność czasowa rozwiązania wynosi O(n^2*p), złożoność pamięciowa: O(np).
"""

from zad4testy import runtests


def select_buildings(T,p):
    n = len(T)
    sort_key = lambda i: T[i][1]

    original_indices = [i for i in range(n)]
    original_indices = sorted(original_indices, key=sort_key)

    stud = [(el[2]-el[1])*el[0] for el in T]
    F = [[0 for _ in range(p+1)] for _ in T]
    P = [[-1 for _ in range(p+1)] for _ in T]

    t = stud[original_indices[0]]
    for price in range(T[original_indices[0]][3], p+1):
        F[0][price] = t
    
    for i in range(1, n):
        i_ind = original_indices[i]
        stud_val = stud[i_ind]
        for j in range(i):
            for price in range(T[i_ind][3], p+1):
                curr = stud_val
                try_parent = j
                try_price = price-T[i_ind][3]
                while try_parent != -1:
                    t_ind = original_indices[try_parent]
                    org_price = try_price
                    if T[t_ind][2] < T[i_ind][1] and try_price - T[t_ind][3] >= 0:
                        try_price -= T[t_ind][3]
                        curr += stud[t_ind]
                    try_parent = P[try_parent][org_price]
                
                if curr > F[i][price]:
                    F[i][price] = curr
                    P[i][price] = j if curr > stud_val else -1

    max_ind = 0
    for i in range(n):
        if F[i][p] > F[max_ind][p]:
            max_ind = i

    try_parent = P[max_ind][p]
    i_ind = original_indices[max_ind]
    try_price = p-T[i_ind][3]
    res_list = [i_ind]
    while try_parent != -1:
        t_ind = original_indices[try_parent]
        org_price = try_price
        if T[t_ind][2] < T[i_ind][1]:
            try_price -= T[t_ind][3]
            res_list.append(t_ind)
        try_parent = P[try_parent][org_price]
    
    return res_list


runtests( select_buildings )

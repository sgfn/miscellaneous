"""
Dana jest tablica T[N] wypełniona niepowtarzającymi się liczbami naturalnymi.
Proszę zaimplementować funkcję trojki(T) która zlicza wszystkie trójki liczb,
które spełniają następujące warunki:
(1) największym wspólnym dzielnikiem trzech liczb jest liczba 1,
(2) pomiędzy dwoma kolejnymi elementami trójki może być co najwyżej jedna przerwa.
Funkcja powinna zwrócić liczbę znalezionych trójek.
"""


def nwd(a, b):
    if a == None:
        return b
    elif b == None:
        return a
    while b > 0:
        t = b
        b = a % b
        a = t
    return a


def nwd_trzech(a, b, c):
    # apparently chodzi o coś takiego
    return max(nwd(a, b), nwd(b, c), nwd(a, c))


def rek(T, i, ile, par1, par2, par3, przerwa):
    if ile == 3:
        return 1 if nwd_trzech(par1, par2, par3) == 1 else 0
    if i == len(T):
        return 0
    if przerwa:
        if ile == 1:
            par2 = T[i]
        elif ile == 2:
            par3 = T[i]
        return rek(T, i+1, ile+1, par1, par2, par3, False)
    if ile == 0:
        return rek(T, i+1, ile+1, T[i], par2, par3, False) + rek(T, i+1, ile, par1, par2, par3, False)
    if ile == 1:
        return rek(T, i+1, ile+1, par1, T[i], par3, False) + rek(T, i+1, ile, par1, par2, par3, True)
    if ile == 2:
        return rek(T, i+1, ile+1, par1, par2, T[i], False) + rek(T, i+1, ile, par1, par2, par3, True)

def trojki(T):
    return rek(T, 0, 0, None, None, None, False)


if __name__ == '__main__':
    T = [2, 3, 4, 5, 6, 8, 7]
    print(trojki(T))

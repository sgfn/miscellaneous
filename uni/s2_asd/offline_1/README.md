# Zadanie offline 1
**Szablon rozwiązania:** `zad1.py`

---

Węzły jednokierunkowej listy odsyłaczowej reprezentowane są w postaci:
```
class Node:
    def __init__(self):
        self.val = None     # przechowywana liczba rzeczywista
        self.next = None    # odsyłacz do nastepnego elementu
```

Niech *p* będzie wskaźnikiem na niepustą listę odsyłaczową zawierającą parami
różne liczby rzeczywiste - *a*<sub>1</sub>,*a*<sub>2</sub>,...,*a<sub>n</sub>*
(lista nie ma wartownika).
Mówimy, że lista jest *k*-chaotyczna, jeśli dla każdego elementu zachodzi, że po
posortowaniu listy znalazłby się na pozycji różniącej się od bieżącej o najwyżej
*k*. Tak więc 0-chaotyczna lista jest posortowana, przykładem 1-chaotycznej listy
jest 1,0,3,2,4,6,5, a (*n*-1)-chaotyczna lista długości *n* może zawierać liczby
w dowolnej kolejności. Proszę zaimplementować funkcję `SortH(p, k)`, która
sortuje *k*-chaotyczną listę wskazywaną przez *p*. Funkcja powinna zwrócić
wskazanie na posortowaną listę. Algorytm powinien być jak najszybszy oraz używać
jak najmniej pamięci (w sensie asymptotycznym, mierzonym względem długości *n*
listy oraz parametru *k*). Proszę skomentować jego złożoność czasową dla
*k* = Θ(1), *k* = Θ(log *n*) oraz *k* = Θ(*n*).

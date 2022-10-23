# Kolokwium 1: Zadanie A
**Szablon rozwiązania:** `kol1a.py`

**Złożoność akceptowalna:** *O*(*N* log *N*) lub *O*(*nk*), gdzie *N* to łączna
długość napisów w tablicy wejściowej, *n* to liczba wyrazów, a *k* to długość
najdłuższego słowa.

**Złożoność wzorcowa:** *O*(*N* + *n* log *n*), gdzie *N* to łączna długość
napisów w tablicy wejściowej, a *n* to liczba wyrazów.

---

Mówimy, że dwa napisy są sobie równoważne, jeśli albo są identyczne, albo byłyby
identyczne, gdyby jeden z nich zapisać od tyłu. Na przykład napisy "kot" oraz
"tok" są sobie równoważne, podobnie jak napisy "pies" i "pies". Dana jest
tablica *T* zawierająca *n* napisów o łącznej długości *N* (każdy napis zawiera
co najmniej jeden znak, więc *N* ≥ *n*; każdy napis składa się wyłącznie z
małych liter alfabetu łacińskiego). Siłą napisu *T*[*i*] jest liczba indeksów
*j* takich, że napisy *T*[*i*] oraz *T*[*j*] są sobie równoważne. Napis *T*[*i*]
jest najsilniejszy, jeśli żaden inny napis nie ma większej siły.

Proszę zaimplementować funkcję `g(T)`, która zwraca siłę najsilniejszego napisu
z tablicy *T*. Na przykład dla wejścia:
```
    #     0       1       2      3        4      5       6
    T = ["pies", "mysz", "kot", "kogut", "tok", "seip", "kot"]
```
wywołanie `g(T)` powinno zwrócić 3. Algorytm powinien być możliwie jak najszybszy.
Proszę podać złożoność czasową i pamięciową zaproponowanego algorytmu.

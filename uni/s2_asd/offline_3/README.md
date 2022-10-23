# Zadanie offline 3
**Szablon rozwiązania:** `zad3.py`

---

Mamy daną *N*-elementową tablicę *T* liczb rzeczywistych, w której liczby
zostały wygenerowane z pewnego rozkładu losowego. Rozkład ten mamy zadany jako
*k* przedziałów [*a*<sub>1</sub>,*b*<sub>1</sub>],[*a*<sub>2</sub>,*b*<sub>2</sub>]
,...,[*a<sub>k</sub>,b<sub>k</sub>*] takich, że *i*-ty przedział jest wybierany z
prawdopodobieństwem *c<sub>i</sub>*, a liczba z przedziału
(*x* ∈ [*a<sub>i</sub>,b<sub>i</sub>*]) jest losowana zgodnie z rozkładem
jednostajnym. Przedziały mogą na siebie nachodzić. Liczby
*a<sub>i</sub>,b<sub>i</sub>* są liczbami naturalnymi ze zbioru {1,...,*N*}.

Proszę zaimplementować funkcję `SortTab(T, P)` sortującą podaną tablicę i
zwracającą posortowaną tablicę jako wynik. Pierwszy argument to tablica do
posortowania, a drugi to opis przedziałów w postaci:
```
    P = [(a_1, b_1, c_1), (a_2, b_2, c_2), ..., (a_k, b_k, c_k)]
```
Na przykład dla wejścia:
```
    T = [6.1, 1.2, 1.5, 3.5, 4.5, 2.5, 3.9, 7.8]
    P = [(1, 5, 0.75), (4, 8, 0.25)]
```
po wywołaniu `SortTab(T, P)` tablica zwrócona w wyniku powinna mieć postać:
```
    T = [1.2, 1.5, 2.5, 3.5, 3.9, 4.5, 6.1, 7.8]
```
Algorytm powinien być możliwie jak najszybszy. Proszę podać złożoność czasową i
pamięciową zaproponowanego algorytmu.

# Zadanie offline 2
**Szablon rozwiązania:** `zad2.py`

---

Dany jest ciąg przedziałów domkniętych *L* = [[*a*<sub>1</sub>,*b*<sub>1</sub>],
...,[*a<sub>n</sub>,b<sub>n</sub>*]]. Początki i końce przedziałów są liczbami
naturalnymi. Poziomem przedziału *c* ∈ *L* nazywamy liczbę przedziałów w *L*,
które w całości zawierają się w *c* (nie licząc samego *c*). Proszę zaproponować
i zaimplementować algorytm, który zwraca maksimum z poziomów przedziałów
znajdujących się w *L*. Proszę uzasadnić poprawność algorytmu i oszacować jego
złożoność obliczeniową.

Algorytm należy zaimplementować jako funkcję postaci:
```
    def depth ( L ):
        ...
```
która przyjmuje listę przedziałów `L` i zwraca maksimum z poziomów przedziałów
w `L`.

**Przykład.**   Dla listy przedziałów:
```
    L = [[1, 6],
         [5, 6],
         [2, 5],
         [8, 9],
         [1, 6]]
```
wynikiem jest liczba 3.

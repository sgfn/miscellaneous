"""
Jakub Pisarek

Rozwiązanie to algorytm zachłanny bazujący na strukturze kolejki priorytetowej,
która wykorzystywana jest w celu znalezienia najlepszej dotychczasowej stacji.
Idziemy liniowo przez tablicę, pamiętając aktualny poziom paliwa w baku. Mijane
niezerowe plamy umieszczamy w kolejce priorytetowej - gdy skończy nam się pa-
liwo, cofamy się w przeszłość, retroaktywnie zatrzymując się i tankując na naj-
większej dotychczasowej plamie. Kończymy przejście, gdy mamy w baku poziom pali-
wa wystarczający do dotarcia do celu. Algorytm jest poprawny, gdyż nie udało mi
się znaleźć kontrprzykładu, co więcej, przechodzi wszystkie testy. Niestety,
brak tu miejsca na formalny dowód jego poprawności.

Złożoność czasowa rozwiązania: O(n log n), złożoność pamięciowa: O(n).
"""

from zad5testy import runtests
from queue import PriorityQueue

def plan(T):
    N = len(T)
    magic_box = PriorityQueue(N)
    result = []
    i = 0
    fuel_tank = 0
    while i + fuel_tank < N-1:
        if T[i] != 0:       magic_box.put( (-T[i], i) )
        if fuel_tank == 0:
            best_fuel, best_i = magic_box.get()
            fuel_tank -= best_fuel
            result.append(best_i)
        fuel_tank -= 1
        i += 1
    return sorted(result)

# zmien all_tests na True zeby uruchomic wszystkie testy
runtests( plan, all_tests = True )

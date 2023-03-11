# RRiR 2022/23 projekt – równanie transportu ciepła

## Ostrzeżenie
Poniższe wyprowadzenie zostało uznane przez prowadzącego o inicjałach TS
za błędne z racji na pominięcie stałej *k* w dalszej części obliczeń.

Osobie potencjalnie korzystającej z niniejszego projektu zaleca się zrobić to poprawnie,
tj. inaczej. Niezastosowanie się grozi utratą 50% pkt z projektu u ww. prowadzącego.

## Wymagania systemowe
- Biblioteka C++ [Armadillo](https://arma.sourceforge.net/) – rozwiązywanie układów równań liniowych
    - instalacja – systemy debianopodobne:

        `sudo apt install libarmadillo-dev`
- [gnuplot](http://www.gnuplot.info/) – rysowanie wykresów
    - instalacja – systemy debianopodobne:

        `sudo apt install gnuplot`


## Budowanie
Wymagany kompilator C++ obsługujący standard C++11.

Kompilacja (przy użyciu `gcc`):

`make`

## Uruchamianie
`./heateq [N]`

N – liczba elementów z przedziału [3, 10000]; domyślnie 3

## Autor
Jakub Pisarek [@sgfn](https://github.com/sgfn)

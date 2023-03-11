##
# @mainpage Triangulacja wielokąta prostego – porównanie metod. Dokumentacja techniczna modułu triangulate
#
# @section description_main Opis
# Moduł <code>triangulate</code> zawiera funkcje triangulujące wielokąty proste metodami podziału na wielokąty y-monotoniczne i Delaunay'a.
#
# @section requirements_main Wymagania techniczne
# - Python >=3.8.10 z zewnętrznymi bibliotekami <code>matplotlib</code> oraz <code>numpy</code>
# - Środowisko Jupyter Notebook
#
# @section libraries_main Biblioteki/Moduły
# - Biblioteka standardowa <code>collections</code> (https://docs.python.org/3/library/collections.html)
#   - Kontener <code>deque</code>
# - Biblioteka standardowa <code>enum</code> (https://docs.python.org/3/library/enum.html)
#   - Typ enumeracyjny <code>Enum</code>
# - Biblioteka standardowa <code>math</code> (https://docs.python.org/3/library/math.html)
#   - Funkcje <code>atan2</code>, <code>fsum</code>
#   - Stałe <code>inf</code>, <code>pi</code>
# - Zewnętrzna biblioteka <code>numpy.linalg</code> (https://numpy.org/doc/stable/reference/routines.linalg.html)
#   - Funkcja <code>det</code>
# - Narzędzie graficzne <code>geometria</code> wraz z własnym jego rozszerzeniem
#   - Biblioteka standardowa <code>json</code>, biblioteki zewnętrzne <code>matplotlib</code>, <code>numpy</code>
#
# @section notes_main Notatki
# - W celu uruchomienia wizualizacji, zaleca się korzystanie z załączonego notebooka Jupyter.
#   Więcej informacji na ten temat znaleźć można w dokumentacji użytkownika i samym notebooku.
# - Informacje nt. obsługi narzędzia graficznego dostarczonego w module <code>geometria</code> nie będą tu udzielane.
#
# @section authors_main Autorzy
# Jakub Pisarek, Szymon Bednorz

##
# @namespace triangulate
#
# @brief Moduł zawiera funkcje triangulujące wielokąty proste metodami podziału na wielokąty y-monotoniczne i Delaunay'a

##
# @file triangulate.py
#
# @brief Funkcje triangulujące wielokąty proste metodami podziału na wielokąty y-monotoniczne i Delaunay'a
#
# @section libraries_triangulate Biblioteki/Moduły
# - Wszystkie wymienione na początku dokumentu


from collections import deque
from enum import Enum
from math import atan2, fsum, inf, pi

from numpy.linalg import det

from geometria import BetterPlot


class VertexType(Enum):
    """! Typ wierzchołka wyznaczony przez klasyfikację"""
    ## Wierzchołek początkowy
    START = 1,
    ## Wierzchołek końcowy
    END = 2,
    ## Wierzchołek łączący
    MERGE = 3,
    ## Wierzchołek dzielący
    SPLIT = 4,
    ## Wierzchołek prawidłowy
    REGULAR = 5


def det_3x3(a, b, c):
    """! Oblicz wyznacznik odpowiedniej macierzy 3x3 dla trójki punktów.
         @param a Współrzędne pierwszego punktu
         @param b Współrzędne drugiego punktu
         @param c Współrzędne trzeciego punktu
         @return wartość obliczonego wyznacznika
    """
    return fsum((a[0]*b[1], b[0]*c[1], c[0]*a[1], -c[0]*b[1], -a[0]*c[1], -b[0]*a[1]))


def find_extremes(polygon):
    """! Znajdź indeksy punktów o największej i najmniejszej współrzędnej y.
         @param polygon   Wielokąt (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego ekstrema należy wyznaczyć
         @return para indeksów, kolejno punktu najwyżej i najniżej położonego
    """
    highest, lowest = 0, 0
    for i in range(1, len(polygon)):
        if polygon[i][1] > polygon[highest][1]:
            highest = i
        if polygon[i][1] < polygon[lowest][1]:
            lowest = i
    return highest, lowest


def is_y_monotone(polygon):
    """! Sprawdź, czy podany wielokąt jest y-monotoniczny.
         @param polygon Wielokąt (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), który należy sprawdzić
         @retval True jeżeli wielokąt jest y-monotoniczny
         @retval False w przeciwnym przypadku
    """
    N = len(polygon)
    highest, lowest = 0, 0
    for i in range(1, N):
        if polygon[i][1] > polygon[highest][1]:
            highest = i
        if polygon[i][1] < polygon[lowest][1]:
            lowest = i

    for side in (1, -1):
        i = highest
        next = -1
        while next != lowest:
            next = i + side
            if next == N:   next = 0
            if next == -1:  next = N-1
            if polygon[next][1] > polygon[i][1]:
                return False
            i = next

    return True


def classify_vertices(polygon, eps=10**(-12)):
    """! Sklasyfikuj wierzchołki wielokąta.
         @param polygon Wielokąt (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego wierzchołki należy sklasyfikować
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista wartości <code>VertexType</code> odpowiadających kolejnym wierzchołkom
    """
    N = len(polygon)
    result = [None for _ in polygon]

    for i in range(N):
        next = i+1 if i != N-1 else 0
        is_agg_or_div = det_3x3(polygon[i-1], polygon[i], polygon[next]) < -eps
        if polygon[i][1] > polygon[next][1] and polygon[i][1] > polygon[i-1][1]:
            vt = VertexType.SPLIT if is_agg_or_div else VertexType.START
        elif polygon[i][1] < polygon[next][1] and polygon[i][1] < polygon[i-1][1]:
            vt = VertexType.MERGE if is_agg_or_div else VertexType.END
        else:
            vt = VertexType.REGULAR

        result[i] = vt

    return result


def triangulate_y_monotone_unsafe(polygon, eps=10**(-12)):
    """! Dokonaj triangulacji wielokąta y-monotonicznego (przyjmuje, że wielokąt jest y-monotoniczny).
         @warning Dla wielokąta, który nie jest y-monotoniczny, działanie funkcji jest niezdefiniowane.
         @param polygon Wielokąt y-monotoniczny (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    tri = []
    events = sorted([i for i, _ in enumerate(polygon)], key=lambda i: -polygon[i][1])
    hst, lst = events[0], events[-1]
    left = (lambda i: i > hst and i < lst) if hst < lst else (lambda i: i > hst or i < lst)

    stack = deque(events[:2])
    for i in events[2:]:
        on_left_chain = left(i)
        if on_left_chain == left(stack[-1]):
            while len(stack) > 1:
                d = det_3x3(polygon[stack[-2]], polygon[stack[-1]], polygon[i])
                # trójkąt jest na zewnątrz wielokąta
                if (on_left_chain and d < -eps) or (not on_left_chain and d > eps):
                    break
                # trójkąt jest wewnątrz wielokąta
                else:
                    tri.append((stack[-2], stack[-1], i) if on_left_chain else (stack[-2], i, stack[-1]))
                    stack.pop()

            stack.append(i)
        else:
            tri.extend(( (i, stack[s+1], stack[s]) if on_left_chain else (i, stack[s], stack[s+1])
                         for s in range(len(stack)-1) ))
            stack = deque((stack[-1], i))

    return tri


def triangulate_y_monotone(polygon, eps=10**(-12)):
    """! Dokonaj triangulacji wielokąta y-monotonicznego.
         @param polygon Wielokąt y-monotoniczny (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
         @return Dla wielokąta, który nie jest y-monotoniczny, zwraca pustą listę.
    """
    if not is_y_monotone(polygon):
        return []
    return triangulate_y_monotone_unsafe(polygon, eps)


def triangulate_y_monotone_with_drawing_data(polygon, drawing_data, eps=10**(-12)):
    """! Dokonaj triangulacji wielokąta y-monotonicznego, generując dodatkowo dane niezbędne do rysowania kolejnych kroków działania algorytmu.
         @param polygon Wielokąt y-monotoniczny (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację należy wyznaczyć
         @param drawing_data Lista, która zostanie wypełniona danymi niezbędnymi do rysowania kolejnych kroków działania algorytmu
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
         @return Dla wielokąta, który nie jest y-monotoniczny, zwraca pustą listę.
    """
    if not is_y_monotone(polygon):
        return []

    drawing_data.clear()
    tri = []
    events = sorted([i for i, _ in enumerate(polygon)], key=lambda i: -polygon[i][1])
    hst, lst = events[0], events[-1]
    left = (lambda i: i > hst and i < lst) if hst < lst else (lambda i: i > hst or i < lst)

    stack = deque(events[:2])
    for i in events[2:]:
        on_left_chain = left(i)
        if on_left_chain == left(stack[-1]):
            while len(stack) > 1:
                drawing_data.append({'stack': [polygon[s] for s in stack], 'result': [(polygon[t1], polygon[t2], polygon[t3]) for t1, t2, t3 in tri], 'triangle': (polygon[stack[-2]], polygon[stack[-1]], polygon[i])})
                d = det_3x3(polygon[stack[-2]], polygon[stack[-1]], polygon[i])
                # trójkąt jest na zewnątrz wielokąta
                if (on_left_chain and d < -eps) or (not on_left_chain and d > eps):
                    break
                # trójkąt jest wewnątrz wielokąta
                else:
                    tri.append((stack[-2], stack[-1], i) if on_left_chain else (stack[-2], i, stack[-1]))
                    stack.pop()

            stack.append(i)
        else:
            for s in range(len(stack)-1):
                drawing_data.append({'stack': [polygon[s] for s in stack], 'result': [(polygon[t1], polygon[t2], polygon[t3]) for t1, t2, t3 in tri], 'triangle': (polygon[i], polygon[stack[s]], polygon[stack[s+1]])})
                # drawing_data.append({'stack': list(stack), 'result': tri.copy(), 'triangle': (i, stack[s], stack[s+1])})
                tri.append((i, stack[s+1], stack[s]) if on_left_chain else (i, stack[s], stack[s+1]))
            stack = deque((stack[-1], i))

    return tri


def triangulate_y_monotone_subpoly_unsafe(polygon, vertices, eps=10**(-12)):
    """! Dokonaj triangulacji pod-wielokąta y-monotonicznego (przyjmuje, że pod-wielokąt jest y-monotoniczny).
         @warning Dla pod-wielokąta, który nie jest y-monotoniczny, działanie funkcji jest niezdefiniowane.
         @param polygon Wielokąt wyjściowy (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara)
         @param vertices Lista indeksów wierzchołków wielokąta wyjściowego tworzących pod-wielokąt y-monotoniczny, którego triangulację należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    remapped_result = triangulate_y_monotone_unsafe([polygon[i] for i in vertices], eps)
    return [(vertices[i], vertices[j], vertices[k]) for (i, j, k) in remapped_result]


def triangulate_y_monotone_subpoly(polygon, vertices, eps=10**(-12)):
    """! Dokonaj triangulacji pod-wielokąta y-monotonicznego.
         @param polygon Wielokąt wyjściowy (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara)
         @param vertices Lista indeksów wierzchołków wielokąta wyjściowego tworzących pod-wielokąt y-monotoniczny, którego triangulację należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
         @return Dla pod-wielokąta, który nie jest y-monotoniczny, zwraca pustą listę.
    """
    # przyklad
    # polygon  0 1 2 3 4 5 6
    # vertices                   2 4 5 6
    # remapped_polygon           0 1 2 3
    # remapped_result                       0 1 2      2 3 0
    # true_result                           2 4 5      5 6 2
    remapped_result = triangulate_y_monotone([polygon[i] for i in vertices], eps)
    return [(vertices[i], vertices[j], vertices[k]) for (i, j, k) in remapped_result]


def triangulate_y_monotone_subpoly_with_drawing_data(polygon, vertices, drawing_data, eps=10**(-12)):
    """! Dokonaj triangulacji pod-wielokąta y-monotonicznego, generując dodatkowo dane niezbędne do rysowania kolejnych kroków działania algorytmu.
         @param polygon Wielokąt wyjściowy (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara)
         @param vertices Lista indeksów wierzchołków wielokąta wyjściowego tworzących pod-wielokąt y-monotoniczny, którego triangulację należy wyznaczyć
         @param drawing_data Lista, która zostanie wypełniona danymi niezbędnymi do rysowania kolejnych kroków działania algorytmu
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
         @return Dla pod-wielokąta, który nie jest y-monotoniczny, zwraca pustą listę.
    """
    remapped_result = triangulate_y_monotone_with_drawing_data([polygon[i] for i in vertices], drawing_data, eps)
    return [(vertices[i], vertices[j], vertices[k]) for (i, j, k) in remapped_result]


def triangulate_partition(polygon, eps=10**(-12)):
    """! Dokonaj triangulacji wielokąta prostego, metodą podziału na wielokąty y-monotoniczne.
         @param polygon Wielokąt prosty (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    def add_edge(fr, to):
        G[fr].add(to)
        G[to].add(fr)

    def get_nearest(state, broom):
        nearest = None
        n_val = -inf
        for i in state:
            # x dla którego y punktu leży na odcinku -- ma być jak największy, lecz nie większy niż x punktu
            x_a, y_a = polygon[i]
            x_b, y_b = polygon[i+1 if i != N-1 else 0]
            x = lambda y: (y - (y_a-(y_a-y_b)/(x_a-x_b)*x_a))/((y_a-y_b)/(x_a-x_b))
            val = x(polygon[broom][1])
            if val < polygon[broom][0] and val > n_val:
                nearest = i
        return nearest

    def the_thing(i, j, k):
        val = atan2(polygon[k][1]-polygon[j][1], polygon[k][0]-polygon[j][0]) - atan2(polygon[j][1]-polygon[i][1], polygon[j][0]-polygon[i][0])
        if val < -pi:
            val += 2*pi
        elif val > pi:
            val -= 2*pi
        return val


    result = []
    N = len(polygon)
    classification = classify_vertices(polygon)
    events = sorted([i for i in range(N)], key=lambda i: -polygon[i][1])

    prevind = lambda i: N-1 if i == 0 else i-1
    nextind = lambda i: 0 if i == N-1 else i+1

    # reprezentacja grafowa wielokąta - lista sąsiedztwa
    G = [{nextind(i)} for i in range(N)]

    # podział na wielokąty y-monotoniczne
    state = {}
    for broom in events:
        v_type = classification[broom]
        if v_type == VertexType.START:
            state[broom] = broom
        elif v_type == VertexType.END:
            if classification[state[prevind(broom)]] == VertexType.MERGE:
                add_edge(broom, state[prevind(broom)])

            state.pop(prevind(broom))
        elif v_type == VertexType.SPLIT:
            nearest = get_nearest(state, broom)
            add_edge(broom, state[nearest])
            state[nearest] = broom
            state[broom] = broom
        elif v_type == VertexType.MERGE:
            prev_vertex = prevind(broom)
            if classification[state[prev_vertex]] == VertexType.MERGE:
                add_edge(broom, state[prev_vertex])
            state.pop(prev_vertex)
            nearest = get_nearest(state, broom)
            if classification[state[nearest]] == VertexType.MERGE:
                add_edge(broom, state[nearest])
            state[nearest] = broom
        else:
            if polygon[prevind(broom)][1] > polygon[broom][1]:
                if classification[state[prevind(broom)]] == VertexType.MERGE:
                    add_edge(broom, state[prevind(broom)])
                state.pop(prevind(broom))
                state[broom] = broom
            else:
                nearest = get_nearest(state, broom)
                if classification[state[nearest]] == VertexType.MERGE:
                    add_edge(broom, state[nearest])
                state[nearest] = broom

    # dokonaj triangulacji y-monotonicznych
    y_monotone_subpolygons = []
    first_non_empty = 0
    while True:
        while first_non_empty < N and len(G[first_non_empty]) == 0:
            first_non_empty += 1
        if first_non_empty == N:
            break

        i = first_non_empty
        j = G[i].pop()
        poly = [i]
        while True:
            poly.append(j)
            k = None
            k_thing = -inf
            for ind in G[j]:
                if ind == i:
                    continue
                thing = the_thing(i, j, ind)
                if thing > k_thing:
                    k_thing = thing
                    k = ind
            assert k is not None
            G[j].remove(k)
            i, j = j, k
            if j == first_non_empty:
                break
        y_monotone_subpolygons.append(poly)

    for subpoly_vertices in y_monotone_subpolygons:
        assert is_y_monotone([polygon[i] for i in subpoly_vertices]), 'polygon not y-monotone!'
        result.extend(triangulate_y_monotone_subpoly(polygon, subpoly_vertices, eps))

    return result


def triangulate_partition_with_drawing_data(polygon, drawing_data, eps=10**(-12)):
    """! Dokonaj triangulacji wielokąta prostego, metodą podziału na wielokąty y-monotoniczne, generując dodatkowo dane niezbędne do rysowania kolejnych kroków działania algorytmu.
         @param polygon Wielokąt prosty (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację należy wyznaczyć
         @param drawing_data Lista, która zostanie wypełniona danymi niezbędnymi do rysowania kolejnych kroków działania algorytmu
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    def add_edge(fr, to):
        G[fr].add(to)
        G[to].add(fr)
        added_edges.append((fr, to))

    def get_nearest(state, broom):
        nearest = None
        n_val = -inf
        for i in state:
            # x dla którego y punktu leży na odcinku -- ma być jak największy, lecz nie większy niż x punktu
            x_a, y_a = polygon[i]
            x_b, y_b = polygon[i+1 if i != N-1 else 0]
            x = lambda y: (y - (y_a-(y_a-y_b)/(x_a-x_b)*x_a))/((y_a-y_b)/(x_a-x_b))
            val = x(polygon[broom][1])
            if val < polygon[broom][0] and val > n_val:
                nearest = i
        return nearest

    def the_thing(i, j, k):
        val = atan2(polygon[k][1]-polygon[j][1], polygon[k][0]-polygon[j][0]) - atan2(polygon[j][1]-polygon[i][1], polygon[j][0]-polygon[i][0])
        if val < -pi:
            val += 2*pi
        elif val > pi:
            val -= 2*pi
        return val


    # drawing_data.append({'stack': list(stack), 'result': tri.copy(), 'triangle': (stack[-2], stack[-1], i)})

    result = []
    N = len(polygon)
    classification = classify_vertices(polygon)
    events = sorted([i for i in range(N)], key=lambda i: -polygon[i][1])

    prevind = lambda i: N-1 if i == 0 else i-1
    nextind = lambda i: 0 if i == N-1 else i+1

    # reprezentacja grafowa wielokąta - lista sąsiedztwa
    G = [{nextind(i)} for i in range(N)]

    # podział na wielokąty y-monotoniczne
    added_edges = []
    state = {}
    for broom in events:
        drawing_data.append({'broom': broom, 'edges': added_edges.copy(), 'result': []})
        v_type = classification[broom]
        if v_type == VertexType.START:
            state[broom] = broom
        elif v_type == VertexType.END:
            if classification[state[prevind(broom)]] == VertexType.MERGE:
                add_edge(broom, state[prevind(broom)])

            state.pop(prevind(broom))
        elif v_type == VertexType.SPLIT:
            nearest = get_nearest(state, broom)
            add_edge(broom, state[nearest])
            state[nearest] = broom
            state[broom] = broom
        elif v_type == VertexType.MERGE:
            prev_vertex = prevind(broom)
            if classification[state[prev_vertex]] == VertexType.MERGE:
                add_edge(broom, state[prev_vertex])
            state.pop(prev_vertex)
            nearest = get_nearest(state, broom)
            if classification[state[nearest]] == VertexType.MERGE:
                add_edge((broom, state[nearest]))
            state[nearest] = broom
        else:
            if polygon[prevind(broom)][1] > polygon[broom][1]:
                if classification[state[prevind(broom)]] == VertexType.MERGE:
                    add_edge(broom, state[prevind(broom)])
                state.pop(prevind(broom))
                state[broom] = broom
            else:
                nearest = get_nearest(state, broom)
                if classification[state[nearest]] == VertexType.MERGE:
                    add_edge(broom, state[nearest])
                state[nearest] = broom

    # drawing_data.append({'broom': None, 'edges': added_edges.copy(), 'result': [], 'ymon': []})
    # dokonaj triangulacji y-monotonicznych
    y_monotone_subpolygons = []
    first_non_empty = 0
    while True:
        while first_non_empty < N and len(G[first_non_empty]) == 0:
            first_non_empty += 1
        if first_non_empty == N:
            break

        i = first_non_empty
        j = G[i].pop()
        poly = [i]
        while True:
            poly.append(j)
            k = None
            k_thing = -inf
            for ind in G[j]:
                if ind == i:
                    continue
                thing = the_thing(i, j, ind)
                if thing > k_thing:
                    k_thing = thing
                    k = ind
            assert k is not None
            G[j].remove(k)
            i, j = j, k
            if j == first_non_empty:
                break
        y_monotone_subpolygons.append(poly)

    drawing_data.append({'broom': None, 'edges': added_edges.copy(), 'result': [], 'ymon': y_monotone_subpolygons.copy()})

    for subpoly_vertices in y_monotone_subpolygons:
        assert is_y_monotone([polygon[i] for i in subpoly_vertices]), 'polygon not y-monotone!'
        dd = []
        res = triangulate_y_monotone_subpoly_with_drawing_data(polygon, subpoly_vertices, dd, eps)
        drawing_data.append(dd.copy())
        result.extend(res)

    return result


def inside_circle(cp1, cp2, cp3, p, eps=10**(-12)):
    """! Sprawdź, czy podany punkt leży wewnątrz okręgu opisanego na podanym trójkącie.
         @param cp1 Współrzędne pierwszego punktu trójkąta
         @param cp2 Współrzędne drugiego punktu trójkąta
         @param cp3 Współrzędne trzeciego punktu trójkąta
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @param p Współrzędne testowanego punktu
         @retval True jeżeli punkt leży wewnątrz okręgu opisanego na podanym trójkącie
         @retval False w przeciwnym przypadku
    """
    return det([
        [cp1[0], cp1[1], cp1[0]**2+cp1[1]**2, 1],
        [cp2[0], cp2[1], cp2[0]**2+cp2[1]**2, 1],
        [cp3[0], cp3[1], cp3[0]**2+cp3[1]**2, 1],
        [p[0],   p[1],   p[0]**2+p[1]**2,     1]]) > eps


def triangulate_delaunay(polygon, eps=10**(-12)):
    """! Dokonaj triangulacji Delaunay'a wielokąta prostego.
         @param polygon Wielokąt prosty (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację Delaunay'a należy wyznaczyć
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    getuniqeid = lambda pi1, pi2: (min(pi1, pi2), max(pi1, pi2))
    getuniqeids = lambda tt: (getuniqeid(tt[1], tt[2]), getuniqeid(tt[0], tt[2]), getuniqeid(tt[0], tt[1]))
    ensure_ccw = lambda pi1, pi2, pi3: ((pi1, pi3, pi2) if det_3x3(ext_poly[pi1], ext_poly[pi2], ext_poly[pi3]) < eps else (pi1, pi2, pi3))

    N = len(polygon)
    x_min, x_max = inf, -inf
    y_min, y_max = inf, -inf
    for pt in polygon:
        x_min, x_max = min(x_min, pt[0]), max(x_max, pt[0])
        y_min, y_max = min(y_min, pt[1]), max(y_max, pt[1])
    x_span, y_span = x_max-x_min, y_max-y_min
    s1, s2, s3 = (x_min-2*x_span, y_min-y_span), (x_max+2*x_span, y_min-y_span), (0, y_max+y_span)

    # dodawanie największego trójkąta
    ext_poly = polygon.copy()
    ext_poly.extend((s1, s2, s3))
    triangulation = [(N, N+1, N+2)]

    for pi, p in enumerate(ext_poly):
        # wykrywanie złych trójkątów i niepowtarzalnych krawędzi spośród nich
        bad = [i for i, (ti1, ti2, ti3) in enumerate(triangulation) if inside_circle(ext_poly[ti1], ext_poly[ti2], ext_poly[ti3], p)]
        sl = {}
        for badtrind in bad:
            ti1, ti2, ti3 = triangulation[badtrind]
            eids = getuniqeid(ti2, ti3), getuniqeid(ti1, ti3), getuniqeid(ti1, ti2)
            for eidx in eids:
                sl[eidx] = (sl[eidx]+1) if eidx in sl else 1

        # usuwanie złych trójkątów
        toremove = [triangulation[bind] for bind in bad]
        for tri in toremove:
            triangulation.remove(tri)
        triangulation.extend((ensure_ccw(pi, s[0], s[1]) for s, count in sl.items() if count == 1))

    # usuwanie największego trójkąta
    bad = [i for i, (ti1, ti2, ti3) in enumerate(triangulation) if ti1 >= N or ti2 >= N or ti3 >= N]
    toremove = [triangulation[bind] for bind in bad]
    for tri in toremove:
        triangulation.remove(tri)
    return triangulation


def triangulate_delaunay_with_drawing_data(polygon, drawing_data, eps=10**(-12)):
    """! Dokonaj triangulacji Delaunay'a wielokąta prostego, generując dodatkowo dane niezbędne do rysowania kolejnych kroków działania algorytmu.
         @param polygon Wielokąt prosty (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego triangulację Delaunay'a należy wyznaczyć
         @param drawing_data Lista, która zostanie wypełniona danymi niezbędnymi do rysowania kolejnych kroków działania algorytmu
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika (domyślnie 10^-12)
         @return lista trzyelementowych krotek z indeksami wierzchołków tworzących pojedynczy trójkąt z utworzonej triangulacji.
         @return Wierzchołki uzyskanych trójkątów są wymieniane w kolejności przeciwnej do ruchu wskazówek zegara.
    """
    drawing_data.clear()
    getuniqeid = lambda pi1, pi2: (min(pi1, pi2), max(pi1, pi2))
    getuniqeids = lambda tt: (getuniqeid(tt[1], tt[2]), getuniqeid(tt[0], tt[2]), getuniqeid(tt[0], tt[1]))
    ensure_ccw = lambda pi1, pi2, pi3: ((pi1, pi3, pi2) if det_3x3(ext_poly[pi1], ext_poly[pi2], ext_poly[pi3]) < eps else (pi1, pi2, pi3))

    N = len(polygon)
    x_min, x_max = inf, -inf
    y_min, y_max = inf, -inf
    for pt in polygon:
        x_min, x_max = min(x_min, pt[0]), max(x_max, pt[0])
        y_min, y_max = min(y_min, pt[1]), max(y_max, pt[1])
    x_span, y_span = x_max-x_min, y_max-y_min
    s1, s2, s3 = (x_min-2*x_span, y_min-y_span), (x_max+2*x_span, y_min-y_span), (0, y_max+y_span)

    # dodawanie największego trójkąta
    ext_poly = polygon.copy()
    ext_poly.extend((s1, s2, s3))
    triangulation = [(N, N+1, N+2)]

    for pi, p in enumerate(ext_poly):
        # wykrywanie złych trójkątów i niepowtarzalnych krawędzi spośród nich
        bad = [i for i, (ti1, ti2, ti3) in enumerate(triangulation) if inside_circle(ext_poly[ti1], ext_poly[ti2], ext_poly[ti3], p)]
        drawing_data.append({'lims': (s1, s2, s3), 'result': [(ext_poly[t1], ext_poly[t2], ext_poly[t3]) for t1, t2, t3 in triangulation], 'bad': bad.copy(), 'p': p})
        sl = {}
        for badtrind in bad:
            ti1, ti2, ti3 = triangulation[badtrind]
            eids = getuniqeid(ti2, ti3), getuniqeid(ti1, ti3), getuniqeid(ti1, ti2)
            for eidx in eids:
                sl[eidx] = (sl[eidx]+1) if eidx in sl else 1

        # usuwanie złych trójkątów
        toremove = [triangulation[bind] for bind in bad]
        for tri in toremove:
            triangulation.remove(tri)
        triangulation.extend((ensure_ccw(pi, s[0], s[1]) for s, count in sl.items() if count == 1))

    # usuwanie największego trójkąta
    bad = [i for i, (ti1, ti2, ti3) in enumerate(triangulation) if ti1 >= N or ti2 >= N or ti3 >= N]
    toremove = [triangulation[bind] for bind in bad]
    for tri in toremove:
        triangulation.remove(tri)
    return triangulation


def plot_polygon(polygon, classify=True, triangulate='partition', show_steps=False, eps=10**(-12)):
    """! Utwórz obiekt <code>geometria.Plot</code> z wizualizacją wielokąta.
         @param polygon Wielokąt (lista wierzchołków zadanych przeciwnie do ruchu wskazówek zegara), którego wizualizację należy utworzyć
         @param classify Umieść na wizualizacji również klasyfikację wierzchołków (domyślnie <code>True</code>)
         @param triangulate Umieść na wizualizacji również triangulację wielokąta (opcje: <code>'partition'</code>, <code>'delaunay'</code>, <code>None</code>; domyślnie <code>'partition'</code>)
         @param show_steps Umieść na wizualizacji poszczególne kroki algorytmu triangulacji (domyślnie <code>False</code>)
         @param eps Tolerancja dla zera przy porównywaniu wartości wyznacznika podczas triangulacji (domyślnie 10^-12)
         @return obiekt <code>geometria.Plot</code> przechowujący wizualizację wielokąta
    """
    def plot_polygon_show_steps(polygon, classify, triangulate, eps):
        N = len(polygon)
        consecutive = lambda i, j: abs(i-j) in (1, N-1)
        pts = lambda li: [polygon[i] for i in li]
        vsize = 30
        b = BetterPlot()
        b.add_polygon(polygon, draw_pts=(not classify), w=.5, s=10)
        if classify:
            cls = classify_vertices(polygon)
            for tp, clr in COLOUR_MAPPING.items():
                b.add_pts(*(polygon[i] for i, t in enumerate(cls) if t == tp), c=clr, s=vsize)
        if triangulate is not None:
            drawing_data = []
            if triangulate == 'partition':
                triangulation = triangulate_partition_with_drawing_data(polygon, drawing_data, eps)
                next_is_many = False
                for ddentry in drawing_data:
                    if next_is_many:
                        for ddsubentry in ddentry:
                            b.add_polygon(polygon, draw_pts=True, w=.5, s=10)
                            b.add_pts(*ddsubentry['stack'], c='red', s=30)
                            for tri in ddsubentry['result']:
                                b.add_polygon(tri, c='blue', w=1)
                            b.add_polygon(ddsubentry['triangle'], c='red', w=2)
                            b.set_limits((-10, 10)).save_scene_cls()
                    elif 'ymon' in ddentry:
                        b.add_polygon(polygon, draw_pts=True, w=.5, s=10)
                        next_is_many = True
                        for poly in ddentry['ymon']:
                            b.add_polygon([polygon[i] for i in poly], c='green')
                        b.set_limits((-10, 10)).save_scene_cls()
                    else:
                        b.add_polygon(polygon, draw_pts=True, w=.5, s=10)
                        evpt = polygon[ddentry['broom']]
                        b.add_pts(evpt, c='red', s=20)
                        b.add_lines(((-10, evpt[1]), (10, evpt[1])), c='red', draw_pts=False)
                        b.add_lines(*((polygon[pi], polygon[pj]) for (pi, pj) in ddentry['edges']), c='blue')
                        b.set_limits((-10, 10)).save_scene_cls()



            elif triangulate == 'delaunay':
                triangulation = triangulate_delaunay_with_drawing_data(polygon, drawing_data, eps)
                s1, s2, s3 = drawing_data[0]['lims']
                xlims = (min((s1[0], s2[0], s3[0])), max((s1[0], s2[0], s3[0])))
                ylims = (min((s1[1], s2[1], s3[1])), max((s1[1], s2[1], s3[1])))
                for ddentry in drawing_data:
                    for i, tri in enumerate(ddentry['result']):
                        b.add_polygon(polygon, draw_pts=True, w=.5, s=10)
                        b.add_pts(ddentry['p'], s=40, c='orange')
                        if i in ddentry['bad']:
                            b.add_polygon(tri, c='red')
                        else:
                            b.add_polygon(tri, c='blue')
                    b.set_limits(xlims, ylims).save_scene_cls()

            else:
                triangulation = []

            b.add_polygon(polygon, draw_pts=(not classify), w=.5, s=10)
            lines = set()
            for tri in triangulation:
                for i in range(3):
                    if not consecutive(tri[i], tri[i-1]):
                        lines.add((min(tri[i], tri[i-1]), max(tri[i], tri[i-1])))
            b.add_lines(*(pts(ln) for ln in lines), c='green', w=1)
        return b.set_limits((-10, 10)).save_scene_cls().get_plot()


    COLOUR_MAPPING = {VertexType.START:   'green',
                      VertexType.END:     'red',
                      VertexType.MERGE:   'darkblue',
                      VertexType.SPLIT:   'lightblue',
                      VertexType.REGULAR: 'saddlebrown'}

    if show_steps:
        return plot_polygon_show_steps(polygon, classify, triangulate, eps)

    N = len(polygon)
    consecutive = lambda i, j: abs(i-j) in (1, N-1)
    pts = lambda li: [polygon[i] for i in li]
    vsize = 30
    b = BetterPlot()
    b.add_polygon(polygon, draw_pts=(not classify), w=.5, s=10)
    if classify:
        cls = classify_vertices(polygon)
        for tp, clr in COLOUR_MAPPING.items():
            b.add_pts(*(polygon[i] for i, t in enumerate(cls) if t == tp), c=clr, s=vsize)
    if triangulate is not None:
        if triangulate == 'partition':
            triangulation = triangulate_partition(polygon, eps)
        elif triangulate == 'delaunay':
            triangulation = triangulate_delaunay(polygon, eps)
        else:
            triangulation = []

        lines = set()
        for tri in triangulation:
            for i in range(3):
                if not consecutive(tri[i], tri[i-1]):
                    lines.add((min(tri[i], tri[i-1]), max(tri[i], tri[i-1])))
        b.add_lines(*(pts(ln) for ln in lines), c='green', w=1)
    return b.set_limits((-10, 10)).get_plot()

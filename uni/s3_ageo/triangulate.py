import math

from collections import deque

from detlib import *


def find_extremes(polygon):
    highest, lowest = 0, 0
    for i in range(1, len(polygon)):
        if polygon[i][1] > polygon[highest][1]:
            highest = i
        if polygon[i][1] < polygon[lowest][1]:
            lowest = i
    return highest, lowest


def is_y_monotone(polygon):
    N = len(polygon)
    highest, lowest = find_extremes(polygon)

    i = highest
    side = 1
    while side != 0:
        next = i + side
        if next == N:   next = 0
        if next == -1:  next = N-1
        if polygon[next][1] > polygon[i][1]:
            return False
        i = next
        if next == lowest:
            side = -1 if side == 1 else 0
            i = highest

    return True


def classify_vertices(polygon, eps=10**(-12)):
    N = len(polygon)
    result = {'pocz': [], 'konc': [], 'lacz': [], 'dzie': [], 'praw': [], 'list': [None for _ in polygon]}

    for i in range(N):
        next = i+1 if i != N-1 else 0
        is_agg_or_div = det_3x3(polygon[i-1], polygon[i], polygon[next]) < -eps
        if polygon[i][1] > polygon[next][1] and polygon[i][1] > polygon[i-1][1]:
            vertex_is = 'dzie' if is_agg_or_div else 'pocz'
        elif polygon[i][1] < polygon[next][1] and polygon[i][1] < polygon[i-1][1]:
            vertex_is = 'lacz' if is_agg_or_div else 'konc'
        else:
            vertex_is = 'praw'

        result[vertex_is].append(i)
        result['list'][i] = vertex_is

    return result


def triangulate_y_monotone(polygon, eps=10**(-12)):
    result = []
    N = len(polygon)
    sorted_vertices = sorted([i for i in range(N)], key=lambda i: -polygon[i][1])
    highest, lowest = sorted_vertices[0], sorted_vertices[-1]
    consecutive = lambda i, j: abs(i-j) in (1, N-1)
    if highest < lowest:
        left_chain = lambda i: i > highest and i < lowest
    else:
        left_chain = lambda i: i > highest or i < lowest

    stack = deque(sorted_vertices[:2])
    for i in sorted_vertices[2:]:
        currently_left_chain = left_chain(i)
        if currently_left_chain == left_chain(stack[-1]):
            # print(f'{"left" if currently_left_chain else "right"} chain - same')
            while len(stack) > 1:
                # print(f'attempt triangle {stack[-2]} {stack[-1]} {i}')
                d = det_3x3(polygon[stack[-2]], polygon[stack[-1]], polygon[i])
                # triangle is outside polygon
                if (currently_left_chain and d < -eps) or (not currently_left_chain and d > eps):
                    # print('attempted triangle outside polygon - break')
                    break
                # triangle is inside polygon
                else:
                    # print('attempted triangle inside polygon')
                    x = stack.pop()
                    result.append((i, stack[-1]))
            stack.append(i)
        else:
            # print(f'{"left" if currently_left_chain else "right"} chain - different')
            result.extend(((i, s) for s in stack if not consecutive(i, s)))
            stack = deque((stack[-1], i))

    return result

# ZMIEN SPOSOB PRZECHOWYWANIA TRIANGULACJI

# DOES NOT WORK
def triangulate(polygon):
    def add_edge(fr, to):
        result.append((fr, to))
        y_monotone_data['up'][fr] = to
        y_monotone_data['down'][to] = fr


    def get_nearest(state, broom):
        nearest = None
        n_val = -math.inf
        for i in state:
            # x dla którego y punktu leży na odcinku -- ma być jak największy, lecz nie większy niż x punktu
            x_a, y_a = polygon[i]
            x_b, y_b = polygon[i+1 if i != N-1 else 0]
            # y = lambda x: (y_a-y_b)/(x_a-x_b)*x + (y_a-(y_a-y_b)/(x_a-x_b)*x_a)
            x = lambda y: (y - (y_a-(y_a-y_b)/(x_a-x_b)*x_a))/((y_a-y_b)/(x_a-x_b))
            val = x(polygon[broom][1])
            if val < polygon[broom][0] and val > n_val:
                nearest = i
        return nearest


    result = []
    N = len(polygon)
    classification = classify_vertices(polygon)
    c = classification['list']
    events = sorted([i for i in range(N)], key=lambda i: -polygon[i][1])
    prev = lambda i: N-1 if i == 0 else i-1
    consecutive = lambda i, j: abs(i-j) in (1, N-1)

    # podziel na y-monotoniczne
    y_monotone_data = {'up': {}, 'down': {}}
    state = {}
    for broom in events:
        v_type = c[broom]
        # print(f'{state=} {result=} {broom=} {v_type=}')
        # nearest = None
        if v_type == 'pocz':
            state[broom] = broom
        elif v_type == 'konc':
            if c[state[prev(broom)]] == 'lacz':
                # result.append((broom, state[prev(broom)]))
                add_edge(broom, state[prev(broom)])

            state.pop(prev(broom))
        elif v_type == 'dzie':
            nearest = get_nearest(state, broom)
            # result.append((broom, state[nearest]))
            add_edge(broom, state[nearest])
            state[nearest] = broom
            state[broom] = broom
        elif v_type == 'lacz':
            prev_vertex = prev(broom)
            if c[state[prev_vertex]] == 'lacz':
                # result.append((broom, state[prev_vertex]))
                add_edge(broom, state[prev_vertex])
            state.pop(prev_vertex)
            nearest = get_nearest(state, broom)
            if c[state[nearest]] == 'lacz':
                result.append((broom, state[nearest]))
            state[nearest] = broom
        else:
            if polygon[prev(broom)][1] > polygon[broom][1]:
                if c[state[prev(broom)]] == 'lacz':
                    # result.append((broom, state[prev(broom)]))
                    add_edge(broom, state[prev(broom)])
                state.pop(prev(broom))
                state[broom] = broom
            else:
                nearest = get_nearest(state, broom)
                if c[state[nearest]] == 'lacz':
                    # result.append((broom, state[nearest]))
                    add_edge(broom, state[nearest])
                state[nearest] = broom
        # print(f'{nearest=}')

    # idz od najwyzszego, usuwaj krawedzie zewnetrzne.
    # PRIORETYZUJ ZAMYKANIE - jak możesz zamknąć, zamknij
    # jesli idziesz w dol, idz dodanymi w dol jak mozesz.
    # jesli idziesz w gore, idz dodanymi w gore jak mozesz.
    # kazda dodana mozesz isc dokladnie raz w dol i dokladnie raz w gore.
    # jezeli przejdziesz po dodanej dwa razy, usun ja.
    # usun wierzcholki od usunietych krawedzi.

    # dokonaj triangulacji y-monotonicznych
    # print(y_monotone_data)
    y_monotone_polygons = []
    consider_vertex = [True for _ in polygon]
    consider_edge = [True for _ in polygon]
    for broom in events:
        if not consider_vertex[broom]:
            continue
        heading_down = True
        poly = []
        i = broom
        recheck = False
        while True:
            if not recheck:
                poly.append(i)

            get_edge_from = y_monotone_data['down' if heading_down else 'up']
            added_edge = get_edge_from.get(i)
            # prioritise consecutive
            if consecutive(i, broom) and consider_edge[i]:
                added_edge = None

            if added_edge is None:
                if consider_edge[i]:
                    next_i = i+1 if i != N-1 else 0
                    if polygon[i][1] < polygon[next_i][1]:
                        heading_down = False
                        # !!! recheck
                        if not recheck:
                            recheck = True
                            continue
                    consider_edge[i] = False
                    consider_vertex[next_i] = False
                    i = next_i
                else:
                    print('nowhere to go')
                    i = broom
            else:
                get_edge_from.pop(i)
                i = added_edge

            if i == broom:
                break

            recheck = False

        y_monotone_polygons.append(poly)
    print(y_monotone_polygons)

    for polydesc in y_monotone_polygons:
        print(polydesc)
        poly = [polygon[i] for i in polydesc]
        print(is_y_monotone(poly))
        polyres = triangulate_y_monotone(poly)
        result.extend(((polydesc[v_1], polydesc[v_2]) for v_1, v_2 in polyres))

    return result

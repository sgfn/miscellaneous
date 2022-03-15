def parser():
    data = []
    a = input()
    while a:
        dlist = []
        for dig in a:
            dlist.append(int(dig))
        data.append(dlist)
        a = input()
    return data


def d9p1(data):
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))
    v_size = len(data)
    h_size = len(data[0])
    ans = 0
    low_points = []
    for i in range(v_size):
        for j in range(h_size):
            is_low_point = True
            for v_stp, h_stp in steps:
                if 0 <= i+v_stp < v_size and 0 <= j+h_stp < h_size:
                    if data[i+v_stp][j+h_stp] <= data[i][j]:
                        is_low_point = False
                        break
            if is_low_point:
                ans += 1 + data[i][j]
                low_points.append((i, j))
    return ans, low_points


def recursive(data, r, c, used_points=[]):
    # print(f'r={r} c={c}')
    steps = ((-1, 0), (1, 0), (0, -1), (0, 1))
    v_size = len(data)
    h_size = len(data[0])
    val = 1
    for v_stp, h_stp in steps:
        if 0 <= r+v_stp < v_size and 0 <= c+h_stp < h_size:
            if 9 > data[r+v_stp][c+h_stp] > data[r][c]:
                if (r+v_stp, c+h_stp) not in used_points:
                    used_points.append((r+v_stp, c+h_stp))
                    val += recursive(data, r+v_stp, c+h_stp, used_points)
    return val


def compute_basin_size(data, r, c):
    return recursive(data, r, c)


def d9p2(data, low_points):
    a = []
    for r, c in low_points:
        a.append(compute_basin_size(data, r, c))
    b = sorted(a, reverse=True)
    return b[0]*b[1]*b[2]

if __name__ == '__main__':
    data = parser()
    ans_1, aid = d9p1(data)
    # print(ans_1)
    print(d9p2(data, aid))

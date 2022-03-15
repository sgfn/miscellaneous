def parser():
    data = []
    a = input()
    while a:
        row = [int(d) for d in a]
        data.append(row)
        a = input()
    return data


def d11(data):
    steps = ((-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1))
    v_size = len(data)
    h_size = len(data[0])
    counter = 0
    comparison = [[True for _ in range(h_size)] for _ in range(v_size)]

    for it in range(1, 501):
        # print(f'STEP {it}')
        flashing = []
        has_flashed = [[False for _ in range(h_size)] for _ in range(v_size)]

        for i in range(v_size):
            for j in range(h_size):
                if data[i][j] > 9 - it:
                    flashing.append((i, j))
        # print(flashing)

        while flashing:
            r, c = flashing[0]
            if has_flashed[r][c]:
                flashing.pop(0)
                continue
            # print(f'FLASHING {r} {c}')
            has_flashed[r][c] = True
            counter += 1
            for v_step, h_step in steps:
                if 0 <= r+v_step < v_size and 0 <= c+h_step < h_size:
                    data[r+v_step][c+h_step] += 1
                    if data[r+v_step][c+h_step] > 9 - it:
                        if not has_flashed[r+v_step][c+h_step]:
                            flashing.append((r+v_step, c+h_step))
            flashing.pop(0)
        
        for i in range(v_size):
            for j in range(h_size):
                if data[i][j] > 9 - it:
                    data[i][j] = 0 - it
        if has_flashed == comparison:
            print(it)

    return counter        


if __name__ == '__main__':
    data = parser()
    print(d11(data))
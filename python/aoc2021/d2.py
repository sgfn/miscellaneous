def d2(data, aim_mode=False):
    aim = 0
    hor_pos = 0
    depth = 0
    for cmd, val in data:
        if cmd == 'forward':
            if aim_mode:
                depth += aim * int(val)
            hor_pos += int(val)
        elif cmd == 'down':
            if aim_mode:
                aim += int(val)
            else:
                depth += int(val)
        else:
            if aim_mode:
                aim -= int(val)
            else:
                depth -= int(val)
    return hor_pos * depth

if __name__ == '__main__':
    data = []
    a = input()
    while a != '':
        data.append(tuple(a.split()))
        a = input()
    print(d2(data))
    print(d2(data, aim_mode=True))

def d6_slow(data, max_day=80):
    curr = data.copy()
    for day in range(max_day):
        new_fish = 0
        # print(f'day {day}: {curr}')
        for i, fish in enumerate(curr):
            if fish == 0:
                curr[i] = 6
                new_fish += 1
            else:
                curr[i] -= 1
        curr.extend(new_fish * [8])
    return len(curr)

def d6_faster(data, max_day=256):
    amnts = [0 for _ in range(9)]
    for fish in data:
        amnts[fish] += 1
    for day in range(max_day):
        # print(f'day {day}: {amnts}')
        tmp = amnts[0]
        for i in range(1, 9):
            amnts[i-1] = amnts[i]
        amnts[8] = tmp
        amnts[6] += tmp
    return sum(amnts)


if __name__ == '__main__':
    data = [int(val) for val in input().split(',')]
    print(d6_faster(data))
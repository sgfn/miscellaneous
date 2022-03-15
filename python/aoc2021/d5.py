def parser():
    data = []
    a = input()
    while a:
        in_two = a.split(' -> ')
        entry = []
        for point_tuple in in_two:
            entry.extend([int(val) for val in point_tuple.split(',')])
        data.append(entry)
        a = input()
    return data

def d5(data, mode=1):
    counter = 0
    n = 1000
    table = [[0 for _ in range(n)] for _ in range(n)]
    for line in data:
        if line[0] == line[2]:
            for i in range(min(line[1], line[3]), max(line[1], line[3])+1):
                table[i][line[0]] += 1
        elif line[1] == line[3]:
            for i in range(min(line[0], line[2]), max(line[0], line[2])+1):
                table[line[1]][i] += 1
        elif mode==2:
            x_p = line[0]
            y_p = line[1]
            while True:
                table[y_p][x_p] += 1
                if x_p == line[2]:
                    break
                elif x_p > line[2]:
                    x_p -= 1
                else:
                    x_p += 1
                if y_p > line[3]:
                    y_p -= 1
                else:
                    y_p += 1
        # print('\n', line, '\n')
        # for row in table:
        #     print(row)
    for row in table:
        for val in row:
            if val > 1:
                counter += 1
    return counter

if __name__ == '__main__':
    data = parser()
    print(d5(data))
    print(d5(data, mode=2))
def d3p1(data):
    gamma = ''
    epsilon = ''
    for j in range(len(data[0])):
        counter = 0
        for i in range(len(data)):
            if data[i][j] == '1':
                counter += 1
        if counter*2 > len(data):
            gamma += '1'
            epsilon += '0'
        else:
            gamma += '0'
            epsilon += '1'
    return int(gamma, base=2) * int(epsilon, base=2)

def d3p2(data):
    oxy_ok = [True for _ in range(len(data))]
    co2_ok = oxy_ok.copy()
    oxy_amnt = co2_amnt = len(data)

    for j in range(len(data[0])):
        counter = 0
        for i in range(len(data)):
            if oxy_ok[i]:
                if data[i][j] == '1':
                    counter += 1
        if counter*2 >= oxy_amnt:
            for i in range(len(data)):
                if data[i][j] == '0' and oxy_ok[i]:
                    oxy_ok[i] = False
                    oxy_amnt -= 1
        else:
            for i in range(len(data)):
                if data[i][j] == '1' and oxy_ok[i]:
                    oxy_ok[i] = False
                    oxy_amnt -= 1
        if oxy_amnt == 1:
            break

    for j in range(len(data[0])):
        counter = 0
        for i in range(len(data)):
            if co2_ok[i]:
                if data[i][j] == '1':
                    counter += 1
        if counter*2 >= co2_amnt:
            for i in range(len(data)):
                if data[i][j] == '1' and co2_ok[i]:
                    co2_ok[i] = False
                    co2_amnt -= 1
        else:
            for i in range(len(data)):
                if data[i][j] == '0' and co2_ok[i]:
                    co2_ok[i] = False
                    co2_amnt -= 1
        if co2_amnt == 1:
            break
    ans = 1
    for i, val in enumerate(oxy_ok):
        if val:
            ans *= int(data[i], base=2)
            break
    for i, val in enumerate(co2_ok):
        if val:
            ans *= int(data[i], base=2)
            break
    return ans
            


if __name__ == '__main__':
    data = []
    a = input()
    while a != '':
        data.append(a)
        a = input()
    print(d3p1(data))
    print(d3p2(data))

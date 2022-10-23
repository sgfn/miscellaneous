def is_prime(val):
    if val < 2:
        return False
    if val < 4:
        return True
    if val % 2 == 0:
        return False
    i = 3
    while i*i <= val:
        if val % i == 0:
            return False
        i += 2
    return True


def calculate_e(precision=10):
    precision = precision + 5
    e = [0 for _ in range(precision)]
    to_add = [0 for _ in range(precision)]
    to_add[0] = 5
    i = 3
    while max(to_add)>0:
        for ind in range(precision):
            e[ind] += to_add[ind]
            if e[ind] > 9:
                e[ind] %= 10
                e[ind-1] += 1
        r = 0
        for ind in range(precision):
            r = r * 10 + to_add[ind]
            to_add[ind] = (r//i)
            r %= i
        i += 1
    # print('2.', *e[:precision-5], sep='')
    return e[:precision-5]


if __name__ == '__main__':
    precision = 1000
    tab = calculate_e(precision)
    for i in range(precision-10):
        val = 0
        for t in range(10):
            val = val * 10 + tab[i+t]
        if is_prime(val):
            print(val)
            break
            
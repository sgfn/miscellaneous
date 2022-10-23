def is_prime(val):
    if val == 2:
        return True
    if val < 2 or val % 2 == 0:
        return False
    i = 3
    while i*i <= val:
        if val % i == 0:
            return False
        i += 2
    return True


def recursive(T, i=0, val=0):
    if i == len(T):
        return is_prime(val)
    val = val*2 + T[i]
    if val >= 2**31:
        return False
    a = False
    if T[i] == 1 and is_prime(val):
        a = recursive(T, i+1, 0)
    return a or recursive(T, i+1, val)

if __name__ == '__main__':
    T = [1, 1, 1, 0, 1, 1]
    print(recursive(T))
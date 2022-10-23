from random import randint

def is_sum_ok(val):
    if val == 1:
        return True
    i = 2
    while i*i <= val:
        temp = i*i
        while temp < val:
            temp *= i
        i += 1
        if temp == val:
            return True
    return False
    
def zad1(t1, t2):
    n = len(t1)
    left = 0
    while left < n:
        curr_len = 1
        while curr_len < 24 and left+curr_len < n:
            sum = 0
            for i in range(left, left+curr_len):
                sum += t1[i]
            bsum = sum
            left_2 = 0
            while left_2 + 24 - curr_len < n:
                sum = bsum
                for i in range(left_2, left_2+24-curr_len):
                    sum += t2[i]
                if is_sum_ok(sum):
                    print(f'left={left}, curr_len={curr_len}, left_2={left_2}, sum={sum}')
                    return True
                left_2 += 1
            curr_len += 1
        left += 1
    return False

if __name__ == '__main__':
    t1 = [randint(1, 100) for _ in range(100)]
    t2 = [randint(1, 100) for _ in range(100)]
    print(t1)
    print(t2)
    print(zad1(t1, t2))

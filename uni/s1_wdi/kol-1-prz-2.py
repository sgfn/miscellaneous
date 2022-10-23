from random import randint
from math import isqrt

def prime_sieve(val):
    tab = [True for _ in range(val+1)]
    tab[0] = tab[1] = False
    for i in range(2, isqrt(val)):
        if tab[i] == True:
            temp = i*2
            while temp < val+1:
                tab[temp] = False
                temp += i
    return tab

def is_sum_ok(val):
    a = prime_sieve(val//2+1)
    t = len(a)
    for i in range(t):
        if a[i]:
            for j in range(t):
                if a[j]:
                    if val == i*j:
                        return True
    return False
    
def zad2(t1, t2):
    n = len(t1)
    left = 0
    while left < n:
        fr_len = 1
        while left + fr_len < n:
            sum = 0
            for i in range(left, left+fr_len):
                sum += t1[i]
            left_2 = 0
            bsum = sum
            while left_2 + fr_len < n:
                sum = bsum
                for i in range(left_2, left_2 + fr_len):
                    sum += t2[i]
                if is_sum_ok(sum):
                    return True
                left_2 += 1
            fr_len += 1
        left += 1
    return False

if __name__ == '__main__':
    t1 = [randint(1, 100) for _ in range(100)]
    t2 = [randint(1, 100) for _ in range(100)]
    print(t1)
    print(t2)
    print(zad2(t1, t2))
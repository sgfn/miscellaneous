from math import isqrt
from random import randint

def ex17(t1, t2):
    def is_prime(val):
        if val%2 == 0:
            return False
        n = 3
        while n<=isqrt(val):
            if val%n == 0:
                return False
            n += 2
        return True
    
    n = len(t1)
    ans = 0
    for mask in range(3**n):
        sum = 0
        for i in range(n):
            if mask % 3 == 1:
                sum += t1[i]
            elif mask % 3 == 2:
                sum += t2[i]
            else:
                sum += t1[i] + t2[i]
            mask //= 3
        if is_prime(sum):
            ans += 1
            print(sum)
    print()
    return ans

if __name__ == '__main__':
    t1 = [1, 3, 2, 4]
    t2 = [9, 7, 4, 8]
    print(ex17(t1, t2))
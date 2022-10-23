import math

def binsearch_method():
    p = 1
    q = 10
    eps = 1e-12
    while q-p > eps:
        t = (p+q) / 2.0
        if t**t-2020 > 0:
            q = t
        else:
            p = t
    print(p)

def tangents_method():
    i = 5
    i_prev = 0
    eps = 1e-12
    while abs(i-i_prev) >= eps:
        i_prev = i
        i -= (i**i - 2020) / (i**i * (math.log(i)+1))
        
    print(i)

if __name__ == "__main__":
    tangents_method()
    print()
    binsearch_method()
from math import sqrt
a = float(input())
b = float(input())
eps = 10**-8
num=1#DEBUG
while abs(a-b) > eps:
    print(f"a_{num}={a},\tb_{num}={b}")#DEBUG
    num+=1#DEBUG
    old_a = a
    a = sqrt(a*b)
    b = (old_a+b) / 2.0
print(a)
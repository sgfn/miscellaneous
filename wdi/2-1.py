def iloczyn_fib(n):
    if n == 1:
        return True
    c = 1
    d = 1
    while d <= n:
        a = c
        b = d
        while b <= n:
            t = a
            a = a+b
            b = t
            if b*c == n and b != c:
                print(b, c)
                return True
        t = c
        c = c+d
        d = t
    return False

n = int(input())
print(iloczyn_fib(n))
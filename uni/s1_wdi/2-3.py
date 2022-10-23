def pal(n, base=10):
    a = 1
    b = 1
    while n//a > base-1:
        a *= base
    while a>b:
        if (n//a)%base != (n//b)%base:
            return False
        a/=base
        b*=base
    return True

n = int(input())
print(pal(n))
print(pal(n,2))
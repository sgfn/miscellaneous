a = int(input())
b = int(input())
n = int(input())
print(a//b, end='')
p = a % b

if p == 0:
    n = 0
else:
    print('.', end='')

for _ in range(n):
    p *= 10
    print(p//b, end='')
    p %= b
    if p == 0:
        break

print()
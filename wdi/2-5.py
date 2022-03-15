n = int(input())
a = 1
digits = 1
while n//a > 9:
    a *= 10
    digits += 1

num_count = 0
mask = 1

while mask < 2**digits:
    val = 0
    t = mask
    n_pos = 1
    val_pos = 1
    
    while t > 0:
        if t%2 == 1:
            val += ((n//n_pos)%10) * val_pos
            val_pos *= 10
        t //= 2
        n_pos *= 10

    if val % 7 == 0:
        num_count += 1
        # print(val)
    mask += 1

print(num_count)

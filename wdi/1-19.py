eps = 10**-8
e = 1
e_prev = 0
factorial = 1
a = 2
while abs(e-e_prev) > eps:
    print(e) # DEBUG
    e_prev = e
    e += 1/factorial
    factorial *= a
    a += 1
print("final value:", e)
from math import sqrt
a = sqrt(0.5)
pi_value = 2/a
eps = 10**-8
a_prev = 0.0
while abs(a-a_prev) > eps:
    print(pi_value) # DEBUG
    a_prev = a
    a = sqrt(0.5+0.5*a)
    pi_value *= 1/a
print("final value:", pi_value)
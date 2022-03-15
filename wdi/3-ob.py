def dec2sys(n, base):
    symbols = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 
        'A', 'B', 'C', 'D', 'E', 'F')
    ans = ''
    while n > 0:
        next = n % base
        n //= base
        ans = symbols[next] + ans
    return ans

def same_digits(a, b):
    counter_a = [0 for i in range(10)]
    counter_b = counter_a.copy()
    while a > 0:
        counter_a[a%10] += 1
        a //= 10
    while b > 0:
        counter_b[b%10] += 1
        b //= 10
    return True if counter_a == counter_b else False

def prime_sieve(n):
    is_prime = [True for _ in range(n)]
    for i in range(2, n):
        if is_prime[i]:
            j = 2*i
            while j < n:
                is_prime[j] = False
                j += i
            print(i)

def e_value(n):
    val = [0 for _ in range(n+1)]
    val[0] = 1
    comp = val.copy()
    i = 2
    while max(comp) > 0:
        next = 0
        for j in range(n, -1, -1):
            val[j] += comp[j] + next
            next = val[j] // 10
            val[j] %= 10
        next = 0
        for j in range(n+1):
            next += comp[j]
            comp[j] = next//i
            next = next%i*10
        i += 1
    return val

def tenth_value():
    values = [int(val) for val in input().split()]
    m = [0 for _ in range(10)]
    for val in values:
        t = min(m)
        if val > t:
            for i in range(10):
                if m[i] == t:
                    m[i] = val
                    break
    return min(m)

if __name__ == '__main__':
    a = e_value(1000)
    print(a[0], '.', sep='', end='')
    for dig in a[1:]:
        print(dig, end='')
    print()

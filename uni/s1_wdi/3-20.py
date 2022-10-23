def prime_factors(val, tab):
        i = 2
        while val > 1:
            if val % i == 0:
                val //= i
                tab[i] += 1
            else:
                i += 1

def ex20(t):
    max_ans = 0
    n = len(t)
    for i in range(n):
        tab = [0 for _ in range(1000)]
        ans = 0
        j = i
        prime_factors(t[j], tab)
        while max(tab)<2 and j<n-1:
            ans += 1
            j += 1
            prime_factors(t[j], tab)
        if ans > max_ans:
            max_ans = ans
    return max_ans

if __name__ == '__main__':
    print(ex20([2, 23, 33, 35, 7, 4, 6, 7, 5, 11, 13, 22]))
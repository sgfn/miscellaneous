def rozw_int(a, b, n=50):
    ans = 0
    for i in range(n):
        a = (a%b) * 10
        ans = ans*10 + a//b
    return ans

def okr_szuk(rozw, n=50):
    i = 1
    while True:
        baza = rozw // 10**(51-i)
        pr_okr = baza % 10
        calosc = baza
        while calosc < 10**n and calosc != 0:
            calosc = calosc * 10 + pr_okr
        if calosc == rozw:
            print(baza//10, '(', pr_okr, ')')
            return 0
        calosc = baza
        while calosc < 10**n and calosc != 0:
            calosc = calosc * 10**i + baza
        # if calosc
        i += 1

if __name__ == "__main__":
    a = int(input())
    b = int(input())
    rozw = rozw_int(a, b)
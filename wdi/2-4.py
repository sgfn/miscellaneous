def better(n):
    ans = 0
    k = 0
    while 5**k <= n:
        j = 0
        while 3**j * 5**k <= n:
            i = 1
            
            while 2**(i-1) * 3**j * 5**k <= n:
                i *= 2
            
            p = i//2 - 1
            q = i - 1
            while p+1 < q:
                i = (p+q) // 2
                
                if 2**i * 3**j * 5**k <= n:
                    p = i
                else:
                    q = i
            
            ans += p+1
            j += 1
        k += 1

    print(ans)

def fun(n):
    i,j,k = 0,0,0
    counter = 0
    while 2**i <= n:
        j = 0
        while 2**i * 3**j <= n:
            k = 0
            while 2**i * 3**j * 5**k <= n:
                counter += 1
                k += 1
            j += 1
        i += 1

    print(counter)

if __name__ == "__main__":
    n = 3805591701845411843366639787148935861385439694033194839380593733619364789200257198384184973020608204038055917018454118433666397871489358613854396940331948393805937336193647892002571983841849730206082040
    # 200 cyfr
    # fun(n)
    better(n)
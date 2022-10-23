def ex10(t):
    n = len(t)
    ans = 0
    for i in range(n-1):
        r = t[i+1]-t[i]
        j = i+1
        while j<n and t[j] - t[j-1] == r:
            j += 1
        if j-i > ans:
            ans = j-i
    return ans

def zad5dziwnanumeracja(T):
    maxdl=1
    n=len(T)
    for i in range(n-1):
        dl=1
        r=T[i+1]-T[i]
        for j in range(i+1,n):
            if T[j]-T[j-1]==r:
                dl+=1
                if j == n-1:
                    if dl>maxdl:
                        maxdl=dl
                    break
            else:
                if dl>maxdl:
                    maxdl=dl
                break
    return maxdl

if __name__ == '__main__':
    t = [1, 2, 3, 6, 9, 12, 15]
    # print(ex10(t))
    print(zad5dziwnanumeracja(t))
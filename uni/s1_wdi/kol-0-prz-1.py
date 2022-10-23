def multi(T):
    ans = 0
    for entry in T:
        k = len(entry)
        l = 1
        t = k
        while l < k//2+1:
            if entry == entry[0:l]*t:
                if k > ans:
                    ans = k
                    break
            l += 1
            t = k // l
    return ans

if __name__ == '__main__':
    print(multi(['ABCABCABC', 'AAAAAA', 'thisisatest', 'irewtgds']))
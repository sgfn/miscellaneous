def ex18(t):
    def is_pali(i, j):
        while i<=j:
            if t[i] != t[j] or t[i]%2 == 0 or t[j]%2 == 0:
                return False
            i += 1
            j -= 1
        return True
    
    n = len(t)
    ans = 0
    for i in range(n):
        for j in range(i, n):
            if is_pali(i, j):
                ans = max(ans, j-i+1)
    return ans

if __name__ == '__main__':
    t = [2, 4, 6, 1, 1, 3, 7, 3, 1, 5, 19, 2, 4, 4, 4, 4, 4, 4, 4, 4]
    print(ex18(t))

from random import randint
n = int(input())
tab = [randint(100, 999) for _ in range(n)]
# tab = [2, 9, 3, 1, 7, 11, 9, 6, 7, 7, 1, 3, 9, 12, 15]
ans = 1
data = {
    'substring': None,
    'from_pos': None,
    'to_pos': None,
    'from_rev': None,
    'to_rev': None,
}
for i in range(n):
    for j in range(i+1, n):
        changed = False
        ll = j-i+1
        for k in range(i, n-ll+1):
            l = 0
            x = j
            temp = k
            while tab[k] == tab[x]:
                k += 1
                x -= 1
                l += 1
            if l == ll and l > ans:
                ans = l
                changed = True
                data['substring'] = tab[i:j+1]
                data['from_pos'] = i
                data['to_pos'] = j
                data['from_rev'] = temp
                data['to_rev'] = temp+ll-1
        if not changed:
            break

print(tab)
print(ans)
print(data)
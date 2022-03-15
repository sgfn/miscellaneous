from random import randint
n = int(input())
tab = [randint(1, 99) for _ in range(n)]
pos_ans = 1
neg_ans = 1
print(tab)
for i in range(n-1):
    j = i + 1
    r = tab[j] - tab[i]
    l = 1
    while j < n and tab[j] == tab[j-1] + r:
        l += 1
        j += 1
    if r > 0 and l > pos_ans:
        pos_ans = l
        print(f'beg_pos={i} beg={tab[i]} r={r} len={l}')
    elif r < 0 and l > neg_ans:
        neg_ans = l
        print(f'beg_pos={i} beg={tab[i]} r={r} len={l}')
print(abs(pos_ans-neg_ans))
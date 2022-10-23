t = [int(a) for a in input().split()]
n = len(t)
for i in range(n):
    if t[i] == 0:
        br = i
        break

for i in range(br+1):
    if i == 0:
        temp_sum = t[1]+t[2]+t[3]+t[4]
    elif i == 1:
        temp_sum = t[0]+t[2]+t[3]+t[4]
    elif i == br-2:
        temp_sum = t[br-5]+t[br-4]+t[br-3]+t[br-1]
    elif i == br-1:
        temp_sum = t[br-5]+t[br-4]+t[br-3]+t[br-2]
    else:
        temp_sum = t[i-2]+t[i-1]+t[i+1]+t[i+2]
    if temp_sum/4 == t[i]:
        print(t[i])
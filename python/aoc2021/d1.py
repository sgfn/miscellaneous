def d1p1(data):
    prev = -1
    count = 0
    for val in data:
        print(val, end=' ')
        if prev == -1:
            prev = val
            print('(first value)')
        elif val > prev:
            count += 1
            print('(increased)')
        else:
            print('(decreased or no change)')
        prev = val
    print()
    return count

def d1p2(data):
    sum = data[0] + data[1] + data[2]
    count = 0
    print(f'sum 0: {sum} (first value)')
    for i in range(3, len(data)):
        next_sum = sum + data[i] - data[i-3]
        print(f'sum {i-2}: {next_sum}', end=' ')
        if next_sum > sum:
            count += 1
            print('(increased)')
        else:
            print('(decreased or no change)')
        sum = next_sum
    print()
    return count

if __name__ == '__main__':
    data = []
    a = input()
    while a != '':
        data.append(int(a))
        a = input()
    print(d1p2(data))

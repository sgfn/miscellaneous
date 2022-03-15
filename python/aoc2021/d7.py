from random import randint

def calc_using_median(data):
    svals = sorted(data)
    l = len(data)
    median = (svals[l//2-1]+svals[l//2])/2 if l%2 == 0 else svals[l//2]
    if int(median) != median:
        fuel_spent = [0, 0]
        for val in svals:
            fuel_spent[0] += abs(val-int(median))
            fuel_spent[1] += abs(val-int(median)+1)
        tmp = 0 if fuel_spent[0] < fuel_spent[1] else 1
        median_ans = (fuel_spent[tmp], int(median)+tmp)
    else:
        fuel_spent = 0
        for val in svals:
            fuel_spent += abs(val-int(median))
        median_ans = (fuel_spent, int(median))
    return median_ans

def calc_using_average(data):
    l = len(data)
    avg = sum(data) / l
    averages = (int(avg), int(avg)+1)
    fuel_spent = [0, 0]
    for val in data:
        for i in range(2):
            t = abs(val-averages[i])
            fuel_spent[i] += (t*t + t) // 2
    ans = 0 if fuel_spent[0] < fuel_spent[1] else 1
    return fuel_spent[ans], averages[ans]

def manual_tests(n=1000, l=10, max_r=16):
    successes = 0
    for test in range(n):
        vals = [randint(0, max_r) for _ in range(l)]
        # vals = [16, 1, 2, 0, 4, 2, 7, 1, 2, 14]
        avg_ans = calc_using_average(vals)
            
        ans = (1e100, None)
        for pos in range(max_r+1):
            fuel_spent = 0
            for val in vals:
                t = abs(val-pos)
                fuel_spent += (t*t + t) // 2
            if fuel_spent < ans[0]:
                ans = (fuel_spent, pos)
        if avg_ans[0] == ans[0]:
            successes += 1
        else:
            print(f'n={test}\tvals={vals}\n\ta_ans={avg_ans}\tans={ans}')
    return 0 if successes == n else 1

if __name__ == '__main__':
    # manual_tests()
    data = [int(val) for val in input().split(',')]
    print(calc_using_average(data))
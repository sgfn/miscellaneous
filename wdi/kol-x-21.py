from random import randint

def ex21():
    MAX_INT = 10
    MAX = 100
    tab = [randint(1, MAX_INT) for _ in range(MAX)]
    # tab = [1, 2, 3, 4, 12, 6, 7, 8, 9, 10, 11, 5]
    # print(tab)
    
    ans = 0
    counter = 10
    max_val_counter = 0
    prev_max_val = 1001

    while counter > 0:
        max_val = 0
        for val in tab:
            if prev_max_val > val > max_val:
                max_val = val
                max_val_counter = 1
            elif val == max_val:
                max_val_counter += 1
        
        while max_val_counter > 0 and counter > 0:
            ans += max_val
            max_val_counter -= 1
            counter -= 1
        
        prev_max_val = max_val

    return ans


if __name__ == '__main__':
    print(ex21())
from random import randint

def ex1():
    n = int(input())
    tab = [[0 for _ in range(n)] for _ in range(n)]
    row, col, val = 0, 0, 0
    min_row, max_row, min_col, max_col = 0, n-1, 0, n-1
    while min_row <= max_row and min_col <= max_col:
        while col <= max_col:
            tab[row][col] = val
            val += 1
            col += 1
        col -= 1
        min_row += 1
        row += 1
        while row <= max_row:
            tab[row][col] = val
            val += 1
            row += 1
        row -= 1
        max_col -= 1
        col -= 1
        while col >= min_col:
            tab[row][col] = val
            val += 1
            col -= 1
        col += 1
        max_row -= 1
        row -= 1
        while row >= min_row:
            tab[row][col] = val
            val += 1
            row -= 1
        row += 1
        min_col += 1
        col += 1
        
    for row in tab:
        for val in row:
            zeros = "0" if val<10 else ""
            print(zeros, val, sep='', end=' ')
        print()

def ex2(tab):
    def is_ok(val):
        while val>0:
            if val%2 == 0:
                return False
            val //= 10
        return True
    
    for row in tab:
        row_ok = False
        for entry in row:
            if is_ok(entry):
                row_ok = True
                break
        if not row_ok:
            return False
    return True

def ex3(tab):
    def is_ok(val):
        while val>0:
            if val%2 == 0:
                return True
            val //= 10
        return False
    
    for row in tab:
        row_ok = True
        for entry in row:
            if not is_ok(entry):
                row_ok = False
                break
        if row_ok:
            return True
    return False

def ex4(tab, n):
    min_row_sum = 1e100
    max_col_sum = 0
    for i in range(n):
        row_sum = 0
        col_sum = 0
        for j in range(n):
            row_sum += tab[i][j]
            col_sum += tab[j][i]
        if row_sum < min_row_sum:
            min_row_sum = row_sum
            row_ind = i
        if col_sum > max_col_sum:
            max_col_sum = col_sum
            col_ind = j
    return row_ind, col_ind

def ex5(tab, n):
    min_pos_row_ind, max_neg_row_ind, min_col_ind, max_col_ind = None, None, None, None
    min_pos_row_sum = 1e100
    max_neg_row_sum = -1e100
    min_col_sum = 1e100
    max_col_sum = -1e100
    for i in range(n):
        row_sum = 0
        col_sum = 0
        for j in range(n):
            row_sum += tab[i][j]
            col_sum += tab[j][i]
        if row_sum < min_pos_row_sum and row_sum > 0:
            min_pos_row_sum = row_sum
            min_pos_row_ind = i
        if col_sum > max_col_sum:
            max_col_sum = col_sum
            max_col_ind = i
        if row_sum > max_neg_row_sum and row_sum < 0:
            max_neg_row_sum = row_sum
            max_neg_row_ind = i
        if col_sum < min_col_sum:
            min_col_sum = col_sum
            min_col_ind = i
    if max_col_sum/min_pos_row_sum > min_col_sum/max_neg_row_sum:
        return min_pos_row_ind, max_col_ind
    else:
        return max_neg_row_ind, min_col_ind

if __name__ == '__main__':
    n = int(input())
    tab = [[randint(-1e10000,1e10000) for _ in range(n)] for _ in range(n)]
    for row in tab: print(row)
    # print(ex2(tab))
    # print(ex3(tab))
    # print(ex4(tab, n))
    print(ex5(tab, n))
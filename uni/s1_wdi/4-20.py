from random import randint
from math import log10
import os

def rooks(tab):
    n = len(tab)
    max_ans = 0
    row_sums = [0 for _ in range(n)]
    col_sums = [0 for _ in range(n)]
    for i in range(n):
        for j in range(n):
            row_sums[i] += tab[i][j]
            col_sums[i] += tab[j][i]

    row_1 = 0
    col_1 = 0
    while row_1 < n:
        while col_1 < n:
            if col_1 < n-1:
                row_2 = row_1
                col_2 = col_1+1
            else:
                row_2 = row_1+1
                col_2 = 0
            
            while row_2 < n:
                while col_2 < n:
                    if row_1 == row_2:
                        ans = row_sums[row_1]+col_sums[col_1]+col_sums[col_2]
                    elif col_1 == col_2:
                        ans = row_sums[row_1]+row_sums[row_2]+col_sums[col_1] 
                    else:
                        ans = row_sums[row_1]+row_sums[row_2]+col_sums[col_1]+col_sums[col_2] 
                    ans -= 2*(tab[row_1][col_1]+tab[row_2][col_2])
                    
                    if ans > max_ans:
                        max_ans = ans
                        pos = (row_1, col_1, row_2, col_2)

                    col_2 += 1
                row_2 += 1
                col_2 = 0
            col_1 += 1
        row_1 += 1
        col_1 = 0
    return pos, row_sums, col_sums

def print_tab(tab, upper_bound=None, answers=None):
    os.system('clear')
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    max_len = int(log10(upper_bound))+1 if upper_bound else None
    n = len(tab)
    border = '-'*((max_len+2)*n+4) if max_len else '-'*20
    print(f'{border}')
    for i in range(n):
        print('|', end=' ')
        for j in range(n):
            colourcode=''
            endcode = ''
            output_align = ' '
            if max_len:
                curr_len = int(log10(tab[i][j]))+1
                while curr_len < max_len:
                    output_align += ' '
                    curr_len += 1
            if answers:
                if (i, j) == (answers[0][0], answers[0][1]):
                    colourcode = FAIL
                elif (i, j) == (answers[0][2], answers[0][3]):
                    colourcode = FAIL
                elif i==answers[0][0] or i==answers[0][2] or j==answers[0][1] or j==answers[0][3]:
                    colourcode = WARNING
                endcode = ENDC
            
            print(f'{colourcode}{output_align}{tab[i][j]}{endcode}', end=' ')
        if answers[1][i] == min(answers[1]):
            colourcode = OKGREEN
            endcode = ENDC
        else:
            colourcode = ''
            endcode = ''
        print(f' |  {colourcode}{answers[1][i]}{endcode}')
    print(f'{border}\n ', end='')
    for val in answers[2]:
        colourcode = ''
        endcode = ''
        output_align = ' '
        curr_len = int(log10(val))+1
        while curr_len < max_len:
            output_align += ' '
            curr_len += 1
        if val == min(answers[2]):
            colourcode = OKGREEN
            endcode = ENDC
        print(f' {colourcode}{output_align}{val}{endcode}', end='')
    print('\n')

if __name__ == '__main__':
    def main_loop():
        tab = [[randint(1, UPPER_BOUND) for _ in range(N)] for _ in range(N)]
        temp = rooks(tab)
        print_tab(tab, UPPER_BOUND, temp)

    UPPER_BOUND = 1e1
    N = 3
    inp = ''
    while inp != 'q':
        main_loop()
        inp = input('q to quit: ')
    # tab = [[randint(1, UPPER_BOUND) for _ in range(N)] for _ in range(N)]
    # temp = rooks(tab)
    # print_tab(tab, UPPER_BOUND, temp)
    # print(temp[0])

    # THIS IS HOPELESS!
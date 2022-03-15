from copy import deepcopy

def parser():
    dots_data = []
    input_data = []
    a = input()
    mode0 = True
    while a != 'q':
        if a == '':
            mode0=False
            a = input()
            continue
        if mode0:
            dots_data.append(tuple([int(v) for v in a.split(',')]))
        else:
            input_data.append((a[11], a[-1]))
        a = input()

    return dots_data, input_data


def d13(dots_data, inputs):
    size_row = 1311
    size_col = 895
    dots_matrix = [[False for _ in range(size_row)] for _ in range(size_col)]
    for c, r in dots_data:
        dots_matrix[r][c] = True
    
    # print(dots_matrix)
    for inp in inputs:
        if inp[0] == 'x':
            new_dots_matrix = [[False for _ in range(size_row//2)] for _ in range(size_col)]
            for r in range(size_col):
                for c in range(size_row//2):
                    new_dots_matrix[r][c] = dots_matrix[r][c] | dots_matrix[r][size_row-c-1]
            size_row //= 2
        
        else:
            new_dots_matrix = [[False for _ in range(size_row)] for _ in range(size_col//2)]
            for r in range(size_col//2):
                for c in range(size_row):
                    new_dots_matrix[r][c] = dots_matrix[r][c] | dots_matrix[size_col-r-1][c]
            size_col //= 2
                
        dots_matrix = deepcopy(new_dots_matrix)

    

    # print(dots_matrix)
    # print()
    for row in new_dots_matrix:
        for boolean in row:
            if boolean:
                print('#', end='')
            else:
                print('.', end='')
        print()
    
    ans = 0
    for lst in new_dots_matrix:
        for boolean in lst:
            if boolean:
                ans += 1
    return ans

if __name__ == '__main__':
    dots_data, input_data = parser()
    print(input_data)
    print(d13(dots_data, input_data))
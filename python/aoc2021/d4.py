def parser():
    nums = [int(num) for num in input().split(',')]
    row = input()
    boards = []
    board = []
    while row != 'qqq':
        if row == '':
            if board:
                boards.append(board)
            board = []
        else:
            board.append([int(num) for num in row.split()])
        row = input()
    return nums, boards

def d4(nums, boards, mode=1):
    boards_fields = []
    for _ in range(len(boards)):
        boards_fields.append([[False for _ in range(5)] for _ in range(5)])
    mode2_table = [i for i in range(len(boards))]
    for num in nums:
        for b_ind, board in enumerate(boards):
            for b_row, row in enumerate(board):
                for b_col, val in enumerate(row):
                    if val == num:
                        boards_fields[b_ind][b_row][b_col] = True
                        for i in range(6):
                            if min(boards_fields[b_ind][b_row]) == True or i == 5:
                                if mode == 2:
                                    if b_ind not in mode2_table:
                                        break
                                    print(mode2_table)
                                    if len(mode2_table) > 1:
                                        try:
                                            mode2_table.remove(b_ind)
                                        except ValueError:
                                            pass
                                        break
                                    b_ind = mode2_table[0]
                                sum_vals = 0
                                for j in range(25):
                                    if not boards_fields[b_ind][j%5][j//5]:
                                        sum_vals += board[j%5][j//5]
                                return sum_vals * num

                            if boards_fields[b_ind][i][b_col] == False:
                                break


if __name__ == '__main__':
    nums, boards = parser()
    print(d4(nums, boards))
    print(d4(nums, boards, 2))
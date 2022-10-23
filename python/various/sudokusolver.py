from copy import deepcopy

import algorithms.heapsort as hps

input_1 = '010900087\n000200006\n000003210\n001045000\n002108900\n000320600\n093800000\n700001000\n580006090'


def print_board(board):
    print()
    for row in board:
        print(*row, sep='')
    return


def dumb_solver(board, ans_board, ind=0):
    r = ind//9
    c = ind%9
    if 0 <= r <= 2:
        r_st = 0
    elif 3 <= r <= 5:
        r_st = 3
    else:
        r_st = 6
    if 0 <= c <= 2:
        c_st = 0
    elif 3 <= c <= 5:
        c_st = 3
    else:
        c_st = 6

    if ind == 81:
        print_board(ans_board)
        exit()
    if board[r][c] != 0:
        dumb_solver(board, ans_board, ind+1)
        return
    
    while ans_board[r][c] < 9:
        is_ok = True
        ans_board[r][c] += 1
        digit = ans_board[r][c]
        for i in range(9):
            if ((ans_board[r][i] == digit and i != c) 
                or (ans_board[i][c] == digit and i != r)):
                is_ok = False
                break
        if is_ok:
            for i in range(r_st, r_st+2):
                for j in range(c_st, c_st+2):
                    if ans_board[i][j] == digit and i != r and j != c:
                        is_ok = False
                        break
        if is_ok:
            dumb_solver(board, ans_board, ind+1)
    
    ans_board[r][c] = 0


def new_update_cells(cells, r, c, digit, heap_mode=False, backtracking=False):
    change = -1 if backtracking else 1

    if backtracking:
        print('backtracking')
    if 0 <= r <= 2:
        r_st = 0
    elif 3 <= r <= 5:
        r_st = 3
    else:
        r_st = 6
    if 0 <= c <= 2:
        c_st = 0
    elif 3 <= c <= 5:
        c_st = 3
    else:
        c_st = 6

    if heap_mode:
        for cell in cells:
            if (cell['row'] == r or cell['col'] == c or 
                (r_st <= cell['row'] <= r_st+2 and c_st <= cell['col'] <= c_st+2)):
                if backtracking:
                    print(f"updating cell {cell}")
                if backtracking:
                    if cell['values'][digit] == 0:
                        print('IS ZERO, NO CHANGE')
                        continue
                    else:
                        cell['values'][digit] += change
                else:
                    cell['values'][digit] += change
                
                if not backtracking:
                    if cell['values'][digit] == 1:
                        cell['choices'] -= change
                else:
                    if cell['values'][digit] == 0:
                        cell['choices'] -= change
                    print(f"updatet cell {cell}")

    else:
        for i in range(9):
            if cells[r][i]['empty']:
                cells[r][i]['values'][digit] += 1
                if cells[r][i]['values'][digit] == 1:
                    cells[r][i]['choices'] -= 1
            
            if cells[i][c]['empty']:
                cells[i][c]['values'][digit] += 1
                if cells[i][c]['values'][digit] == 1:
                    cells[i][c]['choices'] -= 1
            
        for i in range(r_st, r_st+3):
            for j in range(c_st, c_st+3):
                if cells[i][j]['empty']:
                    cells[i][j]['values'][digit] += 1
                    if cells[i][j]['values'][digit] == 1:
                        cells[i][j]['choices'] -= 1


def new_generate_heap(board):
    cells = [[
        {
            'empty': True,
            'choices': 9,
            'values': {k: 0 for k in range(1, 10)},
            'row': i,
            'col': j,
        } for j in range(9)] for i in range(9)
    ]
    for r, row in enumerate(board):
        for c, digit in enumerate(row):
            if digit != 0:
                cells[r][c]['empty'] = False
                cells[r][c]['choices'] = None
                cells[r][c]['values'] = None
                new_update_cells(cells, r, c, digit)
    
    heap = []
    for i in range(81):
        if cells[i//9][i % 9]['empty']:
            hps.heap_insert(heap, cells[i//9][i % 9], True, True, 'choices')
    
    return heap


def new_recursive_solver(board, heap):
    if len(heap) == 0:
        print_board(board)
        exit()
    
    cell = hps.heap_extract(heap, True, True, 'choices')
    #if cell['choices'] == 0:
    #    print('no choices')
    #    return

    for digit in range(1, 10):
        if cell['values'][digit] == 0:
            board[cell['row']][cell['col']] = digit
            new_update_cells(heap, cell['row'], cell['col'], digit, heap_mode=True)
            heap = hps.heapify(*heap, reverse=True, structures=True, str_ind='choices')
            new_recursive_solver(board, heap)
            break
    new_update_cells(heap, cell['row'], cell['col'], digit, heap_mode=True, backtracking=True)
    print(f'cell before backtracking: {cell}')
    cell['choices'] -= 1
    cell['values'][digit] += 1
    board[cell['row']][cell['col']] = 0

    print(f'cell after backtracking: {cell}')
    heap = hps.heapify(*heap, reverse=True, structures=True, str_ind='choices')
    if cell['choices'] > 0:
        hps.heap_insert(heap, cell, reverse=True, structures=True, str_ind='choices')
    return new_recursive_solver(board, heap)


def generate_heap(board):
    # remade the function so it works on integers instead of booleans
    empty_fields = []
    pointers = [[None for _ in range(9)] for _ in range(9)]
    opt = [[[9, [0 for _ in range(9)]] for _ in range(9)] for _ in range(9)]

    for r, row in enumerate(board):
        for c, digit in enumerate(row):
            # print(f'r={r} c={c} digit={digit}')
            if digit == 0:
                values = [None, None, r, c]
                empty_fields.append(values)
                pointers[r][c] = empty_fields[-1]
            else:
                opt[r][c] = [-1, [1000 for _ in range(9)]]
                pointers[r][c] = [-1, [1000 for _ in range(9)], r, c]
                for i in range(9):
                    opt[r][i][1][digit-1] += 1
                    if opt[r][i][1][digit-1] == 1:
                        opt[r][i][0] -= 1
                    opt[i][c][1][digit-1] += 1
                    if opt[i][c][1][digit-1] == 1:
                        opt[i][c][0] -= 1
                if 0 <= r <= 2:
                    r_st = 0
                elif 3 <= r <= 5:
                    r_st = 3
                else:
                    r_st = 6
                if 0 <= c <= 2:
                    c_st = 0
                elif 3 <= c <= 5:
                    c_st = 3
                else:
                    c_st = 6
                for i in range(r_st, r_st+3):
                    for j in range(c_st, c_st+3):
                        opt[i][j][1][digit-1] += 1
                        if opt[i][j][1][digit-1] == 1:
                            opt[i][j][0] -= 1

    for blank in empty_fields:
        blank[0] = opt[blank[2]][blank[3]][0]
        blank[1] = opt[blank[2]][blank[3]][1]

    return hps.heapify(*empty_fields, reverse=True, structures=True), pointers


def update_cells(pointers, r, c, ind, backtracking=False):
    '''updates cells, what a surprise. required for filling the board'''
    change = -1 if backtracking else 1

    for i in range(9):
        if r == 5 and i == 8:
            print(f'UPD_CLS BEF r=5 c=8 pointers={pointers[r][i]}')
        pointers[r][i][1][ind] += change
        if ((not backtracking and pointers[r][i][1][ind] == 1)
                or (backtracking and pointers[r][i][1][ind] == 0)):
            pointers[r][i][0] -= change
        if r == 5 and i == 8:
            print(f'UPD_CLS AFT r=5 c=8 pointers={pointers[r][i]}')
        if i == 5 and c == 8:
            print(f'UPD_CLS BEF r=5 c=8 pointers={pointers[i][c]}')
        pointers[i][c][1][ind] += change
        if ((not backtracking and pointers[i][c][1][ind] == 1)
                or (backtracking and pointers[i][c][1][ind] == 0)):
            pointers[i][c][0] -= change
        if i == 5 and c == 8:
            print(f'UPD_CLS AFT r=5 c=8 pointers={pointers[i][c]}')

    if 0 <= r <= 2:
        r_st = 0
    elif 3 <= r <= 5:
        r_st = 3
    else:
        r_st = 6
    if 0 <= c <= 2:
        c_st = 0
    elif 3 <= c <= 5:
        c_st = 3
    else:
        c_st = 6
    for i in range(r_st, r_st+3):
        for j in range(c_st, c_st+3):
            if i == 5 and j == 8:
                print(f'UPD_CLS BEF r=5 c=8 pointers={pointers[i][j]}')
            pointers[i][j][1][ind] += change
            if ((not backtracking and pointers[i][j][1][ind] == 1)
                    or (backtracking and pointers[i][j][1][ind] == 0)):
                pointers[i][j][0] -= change
            if i == 5 and j == 8:
                print(f'UPD_CLS AFT r=5 c=8 pointers={pointers[i][j]}')


def not_so_new_recursive_solver(board, heap, pointers):
    # continue recursively until heap empty
    if len(heap) == 0:
        print_board(board)
        exit()

    # extract element of highest priority from heap
    blank = hps.heap_extract(heap, True, True)

    # helper variables to shorten the code
    r = blank[2]
    c = blank[3]
    if (r == 5 and c == 8) or (r == 3 and c == 7) or (r == 2 and c == 7):
        print(f'our digit blank={blank}')
    if -1 in blank[1]:
        print("\t\t\tNEG 1 IN BLANK[1]")
    if blank[0] == -1:
        print("\t\t\tNEG 1 AS VAL OF BLANK[0]")
    # blank[0] -= 1 # we want to do it, but not right now

    # make a copy of blank (might be needed for backtracking)
    new_blank = [blank[0], blank[1].copy(), r, c]

    # iterate over possible values
    for ind, val in enumerate(blank[1]):
        # if r==0 and c==0:
        #     print(blank, '\n', new_blank, '\n\n')
        if val == 0:
            if (r == 5 and c == 8) or (r == 3 and c == 7):
                print(f'\ttrying digit {ind+1}')

            # set value of cell on board, update possibles
            board[r][c] = ind+1
            # blank[0] = 0
            # blank[1] = [0 for _ in range(9)]
            print(f'trying r={r} c={c} digit={ind+1}')
            if r == 3 and c == 7:
                print(heap)
            # delete set value from others' possibles (same row, col, box)
            update_cells(pointers, r, c, ind)

            # remake the heap with the updated values of unfilled cells
            heap = hps.heapify(*heap, reverse=True, structures=True)

            # create a deep copy of heap, possibly not needed
            # heap_copy = deepcopy(heap)
            if r == 3 and c == 7:
                print()
                print(heap)
            # nest function recursively, will print filled board if no errors
            new_recursive_solver(board, heap, pointers)

            # dead end, need to backtrack
            # return the entire heap to previous values
            print(f'backtracking at r={r} c={c} wrong digit={ind+1}')
            update_cells(pointers, r, c, ind, backtracking=True)

            # remove the value from list of possibles
            new_blank[0] -= 1
            new_blank[1][ind] = 1000

            # set the pointer to the updated cell info
            pointers[r][c] = new_blank

            # remake the heap with the reversed and updated values
            hps.heapify(*heap, new_blank, reverse=True, structures=True)


def recursive_solver(board, heap, pointers):
    if len(heap) == 0:
        print_board(board)
        exit()
    # blank = hps.heap_extract(heap, True, True)
    blank = heap[0]
    if blank[0] == 0:
        print('SOMETHINGS OFF')
        print(blank)
        return
    r = blank[2]
    c = blank[3]
    t = blank[0]
    templist = [i for i in range(1, 10) if blank[1][i-1]]
    # for ind, val in enumerate(t[1]):
    print('\t\t\t', templist)
    for aaaa in templist:
        ind = aaaa - 1
        val = True
        hp = deepcopy(heap)
        t = deepcopy(blank)
        pnt = deepcopy(pointers)
        if r == 2 and c == 8:
            print(blank)
            print(f'ind={ind} val={val}')
        if val:
            print(f'poss={blank[0]} list={blank[1]} r={r} c={c}')
            if blank[0] > 1:
                print(f'POSS>1')
                # print(heap)
            blank[0] = 0
            board[r][c] = ind+1
            print(f'\tSETTING r={r} c={c} as {ind+1}')
            for i in range(9):
                if pointers[r][i][1][ind]:
                    pointers[r][i][1][ind] = False
                    pointers[r][i][0] -= 1
                if pointers[i][c][1][ind]:
                    pointers[i][c][1][ind] = False
                    pointers[i][c][0] -= 1
                if 0 <= r <= 2:
                    r_st = 0
                elif 3 <= r <= 5:
                    r_st = 3
                else:
                    r_st = 6
                if 0 <= c <= 2:
                    c_st = 0
                elif 3 <= c <= 5:
                    c_st = 3
                else:
                    c_st = 6
                for i in range(r_st, r_st+3):
                    for j in range(c_st, c_st+3):
                        if pointers[i][j][1][ind]:
                            pointers[i][j][1][ind] = False
                            pointers[i][j][0] -= 1
            hps.heap_extract(heap, reverse=True, structures=True)
            heap = hps.heapify(*heap, reverse=True, structures=True)

            recursive_solver(board, heap, pointers)
            print(f'were back r={r} c={c} set 0, ind={ind}')
            if r == 2 and c == 8:
                print(blank)
                print(heap)
                # print(pointers)
            board[r][c] = 0
            heap = deepcopy(hp)
            pointers[r][c][1][ind] = False
            pointers[r][c][0] -= 1
            # pointers = deepcopy(pnt)
            if r == 2 and c == 8:
                print(heap)
            # hps.heap_insert(heap, blank, reverse=True, structures=True)


def solver(board):
    heap, pointers = generate_heap(board)

    while len(heap) > 0:
        blank = hps.heap_extract(heap, True, True)
        if blank[0] > 1:
            print('MULTIPLE OPTIONS')
            while len(heap) > 0:
                a = hps.heap_extract(heap, True, True)
                print(f'r={a[2]} c={a[3]} possible={a[0]}')
            return 1
        if blank[0] < 1:
            print('NO OPTIONS')
            return 2
        blank[0] = 0
        r = blank[2]
        c = blank[3]

        for ind, val in enumerate(blank[1]):
            if val:
                board[r][c] = ind+1
                for i in range(9):
                    if pointers[r][i][1][ind]:
                        pointers[r][i][1][ind] = False
                        pointers[r][i][0] -= 1
                    if pointers[i][c][1][ind]:
                        pointers[i][c][1][ind] = False
                        pointers[i][c][0] -= 1
                if 0 <= r <= 2:
                    r_st = 0
                elif 3 <= r <= 5:
                    r_st = 3
                else:
                    r_st = 6
                if 0 <= c <= 2:
                    c_st = 0
                elif 3 <= c <= 5:
                    c_st = 3
                else:
                    c_st = 6
                for i in range(r_st, r_st+3):
                    for j in range(c_st, c_st+3):
                        if pointers[i][j][1][ind]:
                            pointers[i][j][1][ind] = False
                            pointers[i][j][0] -= 1
                break
        heap = hps.heapify(*heap, reverse=True, structures=True)
    return 0


if __name__ == '__main__':
    board = []
    print('Solver mode')
    print('Enter the rows, one by one:\n(enter 0 if field is empty)')
    for _ in range(9):
        row = [int(d) for d in input()]
        board.append(row)

    ans_board = deepcopy(board)
    dumb_solver(board, ans_board)
    #heap = new_generate_heap(board)
    #new_recursive_solver(board, heap)
    #heap, pointers = generate_heap(board)
    #new_recursive_solver(board, heap, pointers)
    # print(heap)
    # print()
    # print(pointers)

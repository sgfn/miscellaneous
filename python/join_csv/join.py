import os
# import psutil
import sys
import time


def join(verbose: bool=False, noprint: bool=False) -> int:
    start_t = time.perf_counter()   # get current time for performance tracking

    # Handle erroneous situations
    if len(sys.argv) < 4:
        print('Not enough arguments\nSyntax: join file_path file_path column_name [inner/left/right]')
        return 1

    _, f_path_1, f_path_2, column_name, *args = sys.argv

    if not os.path.isfile(f_path_1):
        print(f'Invalid file path: {f_path_1}')
        return 2
    if not os.path.isfile(f_path_2):
        print(f'Invalid file path: {f_path_2}')
        return 2

    if f_path_1[-4:] != '.csv':
        print(f'Invalid file type: {f_path_1}')
        return 3
    if f_path_2[-4:] != '.csv':
        print(f'Invalid file type: {f_path_2}')
        return 3

    # Set join type - default: inner
    join_type = args[0] if len(args) > 0 else 'inner'

    if join_type not in ('inner', 'left', 'right'):
        print(f'Invalid join type [inner/left/right]: {join_type}')
        return 4

    # Right join is basically left join if you squint a little
    swap_tables = join_type == 'right'
    if swap_tables:     f_path_1, f_path_2 = f_path_2, f_path_1


    with open(f_path_1) as f_1, open(f_path_2) as f_2:
        h_1 = f_1.readline().rstrip('\n').split(',')
        h_2 = f_2.readline().rstrip('\n').split(',')

        if column_name not in h_1 or column_name not in h_2:
            print(f'Invalid column (not present in one or both files): {column_name}')
            return 5
        
        # Some possibly unnecessary dict tomfoolery to create the header row
        h_1_dict = {col: i for i, col in enumerate(h_1)}
        h_2_dict = {col: i for i, col in enumerate(h_2)}
        hdr_p1 = []
        hdr_p2 = []
        for col_1 in h_1:
            # Make sure there are no conflicts in the column names
            if col_1 in h_2_dict and col_1 != column_name:
                col_1 = 'right.'+col_1 if swap_tables else 'left.'+col_1
            hdr_p1.append(col_1)
        
        for col_2 in h_2:
            # No reason to insert the column by which will be joining twice
            if col_2 != column_name:
                if col_2 in h_1_dict:
                    col_2 = 'left.'+col_2 if swap_tables else 'right.'+col_2
                hdr_p2.append(col_2)

        # Get index of join column in both files
        ind_1 = h_1_dict[column_name]
        ind_2 = h_2_dict[column_name]

        # Create a map: join_column key -> bytes of appropriate rows in file_2
        byte_of_key_dict = {}
        current_byte = f_2.tell()   # get current position of file handle
        line = f_2.readline()
        while line:
            row_2 = line.rstrip('\n').split(',')
            key = row_2[ind_2]
            # Can have multiple rows from file_2 matching given key
            if key in byte_of_key_dict:
                byte_of_key_dict[key].append(current_byte)
            else:
                byte_of_key_dict[key] = [current_byte]
            current_byte = f_2.tell()
            line = f_2.readline()

        # Joining done, everything is mapped to everything else just as wanted

        # Get performance tracking data
        # m_used = psutil.Process(os.getpid()).memory_info().rss
        join_t = time.perf_counter()-start_t

        # Print the results
        if not noprint:
            if swap_tables:     print(*hdr_p2, *hdr_p1, sep=',')
            else:               print(*hdr_p1, *hdr_p2, sep=',')

            f_1.seek(0, 0)  # return to the beginning of file_1
            f_1.readline()  # skip the header row

            line = f_1.readline()
            while line:
                row_1 = line.rstrip('\n').split(',')
                key = row_1[ind_1]
                if key in byte_of_key_dict:
                    for byte_offset in sorted(byte_of_key_dict[key]):
                        f_2.seek(byte_offset, 0)
                        row_2 = f_2.readline().rstrip('\n').split(',')
                        # Swap the rows around if performing a right join
                        if swap_tables:
                            print(*row_2[:ind_2], *row_2[ind_2+1:], *row_1,
                                  sep=',')
                        else:
                            print(*row_1, *row_2[:ind_2], *row_2[ind_2+1:],
                                  sep=',')

                # If no matches but join isn't inner, print the row anyway
                elif join_type != 'inner':
                    if swap_tables:
                        print(','*(len(h_2)-1), end='')
                        print(*row_1, sep=',')
                    else:
                        print(*row_1, sep=',', end='')
                        print(','*(len(h_2)-1))
                line = f_1.readline()

    if verbose:
        # d_size = (os.path.getsize(f_path_1)+os.path.getsize(f_path_2))/(1024**2)
        # m_used /= 1024**2
        # print(f"\nPeak memory usage: {round(m_used)} MB ({round((m_used*100)/d_size)}% of overall data size)")
        print(f"Joining time: {round(join_t, 2)} s, total time: {round(time.perf_counter()-start_t, 2)} s")
    return 0


if __name__ == '__main__':
    # join(verbose=True, noprint=True)
    join()

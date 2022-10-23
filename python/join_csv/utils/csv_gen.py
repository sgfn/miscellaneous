import csv
import random
import pickle
import time


def generate_garbage_data(writer, header, columns, amount, w_dict):
    start_t = time.perf_counter()
    w_list = [word for word in w_dict]

    hex_vals = ('0', '1', '2', '3', '4', '5', '6', '7',
                '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')
    company_suffixes = ('Inc.', 'GmbH', 'plc', 'PLC', 'Ltd.', 'LLC', 'L.L.C.',
                        'Corp.', 'Co.', 'Bank', 'Company', 'Union', 'Limited')

    writer.writerow(header)
    print(f'Generating {amount} garbage entries...')

    for i in range(amount):
        print(f'{i+1}/{amount}', end='\r')

        row = []
        for v_type, v_min, v_max, v_prec in columns:
            if   v_type == 'auto_increment':
                row.append(i)

            elif v_type == 'int':
                row.append(random.randint(v_min, v_max))

            elif v_type == 'float':
                shift = 10**v_prec
                row.append(round(random.randint(v_min*shift, v_max*shift)/shift,
                                                v_prec))

            elif v_type == 'hex':
                s = ''
                for _ in range(random.randint(v_min, v_max)):
                    s += random.choice(hex_vals)
                row.append(s)

            elif v_type == 'words':
                out_str = ''
                num_of_words = random.randint(v_min, v_max)

                if num_of_words > 0:
                    out_str = random.choice(w_list)
                    what_to_do = random.randint(1, 10)
                    if   what_to_do < 4:    out_str = out_str.capitalize()
                    elif what_to_do == 10:  out_str = out_str.upper()

                for _ in range(num_of_words-1):
                    app_str = ' ' + random.choice(w_list)
                    what_to_do = random.randint(1, 10)
                    if   what_to_do < 4:    app_str = app_str.capitalize()
                    elif what_to_do == 10:  app_str = app_str.upper()
                    out_str += app_str
                
                if v_prec == 'company':
                    out_str += ' ' +random.choice(company_suffixes)
                    
                row.append(out_str)

        writer.writerow(row)
    print(f'\ndone\nTotal time: {round(time.perf_counter()-start_t, 2)} s\n')
        

if __name__ == '__main__':
    ENTRIES=100_000
    ENTRIES2=100_000

    # Ships are owned by parent companies
    OUT_PATH=f'csv/ships.csv'
    HEADER='ship_id,name,hex,owner_id,value,info'
    COLUMNS=[('auto_increment', None, None, None),
            ('words', 1, 3, None),
            ('hex', 10, 10, None),
            ('int', 0, ENTRIES2-1, None),
            ('float', 0, 100_000_000, 2),
            ('words', 0, 1_000, None)]

    # Why can a company be valued less than its ships combined? Debt, possibly.
    OUT_PATH2=f'csv/owners.csv'
    HEADER2='owner_id,name,hex,value,info'
    COLUMNS2=[('auto_increment', None, None, None),
              ('words', 1, 3, 'company'),
              ('hex', 10, 10, None),
              ('float', -1_000_000_000, 1_000_000_000, 2),
              ('words', 0, 1_000, None)]

    with open('utils/w_dict.pickle', 'rb') as f:    w_dict = pickle.load(f)

    with open(OUT_PATH, 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        generate_garbage_data(writer, HEADER.split(','), COLUMNS, ENTRIES,
                              w_dict)

    with open(OUT_PATH2, 'w', newline='') as out_file:
        writer = csv.writer(out_file, delimiter=',', quoting=csv.QUOTE_MINIMAL)
        generate_garbage_data(writer, HEADER2.split(','), COLUMNS2, ENTRIES2,
                              w_dict)

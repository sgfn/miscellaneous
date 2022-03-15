def parser():
    data = []
    a = input()
    while a:
        entry = a.split()
        data.append(entry)
        a = input()
    return data


def d8p1(data):
    counter = 0
    for entry in data:
        for output_val in entry[-4:]:
            if len(output_val) in (2, 3, 4, 7):
                counter += 1
    return counter


def key_getter(entry):
    default = ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    lens_table = [[] for _ in range(8)]
    for inp_val in entry[:10]:
        lens_table[len(inp_val)].append(inp_val)

    segments_key = {'A': 0, 'B': 0, 'C': 0, 'D': 0, 'E': 0, 'F': 0, 'G': 0}
    certains = {
        'CF': [char for char in lens_table[2][0]],
        'BD': [char for char in lens_table[4][0] if char not in lens_table[2][0]]
        }

    for char in lens_table[3][0]:
        if char not in lens_table[2][0]:
            segments_key['A'] = char
    
    for val in lens_table[6]:
        if certains['CF'][0] in val and certains['CF'][1] in val:
            continue
        for dchar in default:
            if dchar not in val:
                segments_key['C'] = dchar
                segments_key['F'] = certains['CF'][0] if certains['CF'][1] == dchar else certains['CF'][1]

    for val in lens_table[5]:
        if certains['BD'][0] in val and certains['BD'][1] in val:
            for dchar in default:
                if dchar not in val and dchar != segments_key['C']:
                    segments_key['E'] = dchar
    
    for val in lens_table[5]:
        if segments_key['E'] in val:
            for dchar in default:
                if dchar not in val and dchar != segments_key['F']:
                    segments_key['B'] = dchar
                    segments_key['D'] = certains['BD'][0] if certains['BD'][1] == dchar else certains['BD'][1]    
    
    for dchar in default:
        if dchar not in segments_key.values():
            segments_key['G'] = dchar

    return segments_key

def d8p2(data):
    ans = 0
    for entry in data:
        the_key = key_getter(entry)
        val = 0
        for digit in entry[-4:]:
            d = len(digit)
            if d == 2:
                dig = 1
            elif d == 3:
                dig = 7
            elif d == 4:
                dig = 4
            elif d == 7:
                dig = 8
            elif d == 6:
                if the_key['D'] in digit:
                    if the_key['E'] in digit:
                        dig = 6
                    else:
                        dig = 9
                else:
                    dig = 0
            else:
                if the_key['E'] in digit:
                    dig = 2
                elif the_key['B'] in digit:
                    dig = 5
                else:
                    dig = 3
            val = val*10 + dig
        ans += val
    return ans


if __name__ == '__main__':
    data = parser()
    print(d8p2(data))
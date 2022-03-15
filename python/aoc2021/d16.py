def hex2bin(string):
    symbols = {
        '0': '0000',
        '1': '0001',
        '2': '0010',
        '3': '0011',
        '4': '0100',
        '5': '0101',
        '6': '0110',
        '7': '0111',
        '8': '1000',
        '9': '1001',
        'A': '1010',
        'B': '1011',
        'C': '1100',
        'D': '1101',
        'E': '1110',
        'F': '1111'
    }
    ans = ''
    for char in string:
        if char in symbols:
            ans += symbols[char]
    return ans


def bin2dec(string):
    ans = 0
    for char in string:
        ans = ans*2 + int(char)
    return ans


def packet_decoder(string, hex=True, packets_remaining=-1):
    bin_string = hex2bin(string) if hex else string
    if packets_remaining > 0:
        packets_remaining -= 1
    if packets_remaining == 0:
        return
    version = bin2dec(bin_string[:3])
    type_id = bin2dec(bin_string[3:6])
    if type_id == 4:
        i = 6
        bin_val_string = ''
        while bin_string[i] == '1':
            bin_val_string += bin_string[i+1:i+5]
            i += 5
        bin_val_string += bin_string[i+1:i+5]
        i += 5
        val = bin2dec(bin_val_string)

        if '1' in bin_val_string[i:]:
            return packet_decoder(bin_string[i:], False), val
        else:
            return val
    else:
        if bin_string[6] == '0': # don't really wanna combat it right now
            len_in_bits = bin2dec(bin_string[7:22])
            return packet_decoder(bin_string[22:22+len_in_bits], False)
        else:
            len_in_packets = bin2dec(bin_string[7:18])
            return packet_decoder(bin_string[18:], False, len_in_packets)
    


if __name__ == '__main__':
    print(packet_decoder(input()))

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def XOR(a, b):#XOR  for 2 bytes
    st = ''
    for p in range(0, 8):
        st = st + str(int(a[p]) ^ int(b[p]))
    return st


def encode_symbol(symb, layer):  # 1 byte
    st = 0
    mask = '01010101'
    if layer == 2:  # tricky decoding for layer 2
        symb = XOR(symb, mask) # XOR for every 2nd bit
        tmp = symb[7]
        st = int(symb, 2)
        st = st >> 1
        symb = format(st, '08b')
        symb.replace(symb[0], tmp)
    st = int(symb, 2)  # just format 8 bits string to int
    return st


def encode_str(s, layer): #Layer 2
    estr = ''
    for j in range(0, len(s), 8):
        subs = s[j:j + 8]
        estr = estr + chr(encode_symbol(subs, layer))
    return estr


def decode_5_symbols(st, layer):
    r = 0
    if len(st) < 5:
        for n in range(5 - len(st)):
            st = st + 'u'
    for i in range(0, 5):
        r = r + (ord(st[i]) - 33) * pow(85, 4 - i)
    r = format(r, '032b')  # 4 bytes in binary with leading zeros
    # if layer < 3:
    #     r = encode_str(r, layer)
    return r


def layer2(text_binary):
    for i in range(1, len(text_binary), 2):
        text_binary[i] = bool(text_binary[i]) ^ 1
    return text_binary


def check_byte(byte):
    cnt = 0
    byte_return = ''
    for i in range(0, len(byte) - 1):
        if byte[i] == '1':
            cnt = cnt + 1
    bit = int(byte[len(byte) - 1])
    if cnt % 2 == bit:
        byte_return = byte[0:len(byte)-1]
    else:
        byte_return = ''
    return byte_return


def layer3(text_binary):
    output_string = ''
    for i in range(0, len(text_binary), 8):
        byte = check_byte(text_binary[i:i + 8])
        output_string = output_string + byte
    return output_string

def layer1_main():
    f = open("C:/IT/OnionPuzzle/files/layer1.txt", "r")
    message = f.read()
    f.close()
    decoded_string = ''
    decoded_4bytes = ''
    for x in range(0, len(message), 5):
        ch = message[x:x + 5]
        decoded_4bytes = decode_5_symbols(ch, 1)
        decoded_4bytes = encode_str(decoded_4bytes, 1)
        decoded_string = decoded_string + decoded_4bytes
    print('\n' + decoded_string)
    t = open("C:/IT/OnionPuzzle/files/layer1_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()

def layer2_main():
    f = open("C:/IT/OnionPuzzle/files/layer2.txt", "r")
    message = f.read()
    f.close()
    decoded_string = ''
    decoded_4bytes = ''
    for x in range(0, len(message), 5):
        ch = message[x:x + 5]
        decoded_4bytes = decode_5_symbols(ch, 2)
        decoded_4bytes = encode_str(decoded_4bytes, 2)
        decoded_string = decoded_string + decoded_4bytes
    print('\n' + decoded_string)
    t = open("C:/IT/OnionPuzzle/files/layer2_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()


def layer3_main():
    f = open("C:/IT/OnionPuzzle/files/layer3.txt", "r")
    message = f.read()
    f.close()
    decoded_string = ''
    decoded_4bytes = ''
    for x in range(0, len(message), 5):
        ch = message[x:x + 5]
        decoded_4bytes = decode_5_symbols(ch, 3)
        decoded_string = decoded_string + decoded_4bytes
    decoded_string = layer3(decoded_string)
    t = open("C:/IT/OnionPuzzle/files/layer3_middle_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()
    decoded_string = encode_str(decoded_string, 3)
    t = open("C:/IT/OnionPuzzle/files/layer3_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()


def find_key():
    a1 = ''
    b = ''
    c1 = ''
    f = open("C:/IT/OnionPuzzle/files/layer3_middle_response.txt", "r")
    a1 = f.read()
    f.close()
    f = open("C:/IT/OnionPuzzle/files/layer4_middle_response.txt", "r")
    c1 = f.read()
    f.close()
    for i in range(0, 256, 8):
         b = b + XOR(c1[i:i+8], a1[i:i+8])
    # for i in range(376, 512, 8):
    #      b = b + XOR(c1[i:i+8], a1[i:i+8])
    f = open("C:/IT/OnionPuzzle/files/key.txt", "w")
    f.write(b)
    f.close()
    return b


def split_text_by_bytes(text_in_bytes):
    f = open("C:/IT/OnionPuzzle/files/layer4_result_temp2.txt", 'w', encoding="utf-8")
    for z in range(0, len(text_in_bytes), 8):
       f.write(text_in_bytes[z:z+8] + '\n')
    f.close()


def layer4_main():
    f = open("C:/IT/OnionPuzzle/files/layer4.txt", "r")
    message = f.read()
    f.close()
    decoded_string = ''
    decoded_4bytes = ''
    for x in range(0, len(message), 5):
        ch = message[x:x + 5]
        decoded_4bytes = decode_5_symbols(ch, 3)
        decoded_string = decoded_string + decoded_4bytes
    t = open("C:/IT/OnionPuzzle/files/layer4_middle_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()
    key = find_key()
    result = ''
    i = 0
    j = 0
    while i < len(decoded_string):
        j = 0
        while j < len(key) and i < len(decoded_string):
            result = result + XOR(decoded_string[i:i + 8], key[j:j + 8])
            i = i + 8
            j = j + 8
    result = encode_str(result, 1)
    f = open("C:/IT/OnionPuzzle/files/layer4_result.txt", 'w', encoding="utf-8")
    f.write(result)
    f.close()
    return result


# layer1_main()
# layer2_main()
# layer3_main()
# layer4_main()

def header_description():
    ip_version = '0100'#const
    ip_header_size = '0101'#const
    ip_first_byte = '00000000'#no need
    ip_packet_size = '0000000000000000'#valuable info
    ip_id='0000000000000000'#no need
    ip_frag_flag='0000000000000000'#no fragmentation no need
    ip_ttl='00000000'#no need
    ip_udp_iana = '00010001' #UDP = 17
    ip_header_checksum = '0000000000000000' #always correct no need
    ip_sender = '00001010000000010000000100001010' #10.1.1.10
    ip_reseiver = '00001010000000010000000111001000'#10.1.1.200
def ip_header_mask():
    ip_version = '1111'#const
    ip_header_size = '1111'#const
    ip_first_byte = '00000000'#no need
    ip_packet_size = '1111111111111111'#valuable info
    ip_id='0000000000000000'#no need
    ip_frag_flag='0000000000000000'#no fragmentation no need
    ip_ttl='00000000'#no need
    ip_udp_iana = '11111111' #UDP = 17
    ip_header_checksum = '0000000000000000' #always correct no need
    ip_sender = '11111111111111111111111111111111' #10.1.1.10
    ip_reseiver = '11111111111111111111111111111111'#10.1.1.200
    mask = (ip_version + ip_header_size + ip_first_byte +
              ip_packet_size + ip_id + ip_frag_flag + ip_ttl +
              ip_udp_iana + ip_header_checksum + ip_sender + ip_reseiver)
    return mask



#
# f = open("C:/IT/OnionPuzzle/files/layer3.txt", "r")
# message = f.read()
# f.close()
# decoded_string = ''
# decoded_4bytes = ''
# for x in range(0, len(message), 5):
#     ch = message[x:x + 5]
#     decoded_4bytes = decode_5_symbols(ch, 1)
#     decoded_string = decoded_string + decoded_4bytes
# t = open("C:/IT/onion_puzzle/layer3_middle_response.txt", 'w', encoding="utf-8")
# t.write(decoded_string)
# t.close()
# decoded_string = layer3(decoded_string)
# print('\n' + decoded_string)
#
# # print('extra info: ' + str(len(decoded_string)) + decoded_string[258200:len(decoded_string)] + ' chars\n' )
# t = open("C:/IT/onion_puzzle/layer3_response.txt", 'w', encoding="utf-8")
# t.write(decoded_string)  # how to put special characters to file ?
# t.close()
# # See PyCharm help at https://www.jetbrains.com/help/pycharm/

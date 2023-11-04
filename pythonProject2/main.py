# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

def  logical_flip(byte):
    st = ''
    mask = '01010101'
    for i in range(0, 8):  # tricky decoding for layer 2
        st = st + str(int(byte[i]) ^ int(mask[i]))  # XOR for every 2nd bit
    byte = st
    return byte


def encode_symbol(symb, layer): # 1 byte
    st = 0
    if layer == 2:  # tricky decoding for layer 2
        symb = logical_flip(symb)
        tmp = symb[7]
        st = int(symb, 2)
        st = st >> 1
        symb = format(st, '08b')
        symb.replace(symb[0], tmp)
    st = int(symb, 2)  # just format 8 bits string to int
    return st


def encode_str(s, layer):
    estr = ''
    for j in range(0, len(s), 8):
        subs = s[j:j+8]
        estr = estr + chr(encode_symbol(subs, layer))
    return estr


def decode_5_symbols(st, layer):
    r = 0
    if len(st) < 5:
        for n in range(5 - len(st)):
            st = st + 'u'
    for i in range(0, 5):
        r = r + (ord(st[i])-33)*pow(85, 4-i)
    r = format(r, '032b')  # 4 bytes in binary with leading zeros
    r = encode_str(r, layer)
    return r


def layer2(text_binary):
    for i in range(1, len(text_binary), 2):
        text_binary[i] = bool(text_binary[i]) ^ 1
    return text_binary


f = open("C:/IT/OnionPuzzle/files/layer2.txt", "r")
message = f.read()
f.close()
decoded_string = ''
decoded_4bytes = ''
for x in range(0, len(message), 5):
    ch = message[x:x+5]
    decoded_4bytes = decode_5_symbols(ch, 2)
    decoded_string = decoded_string + decoded_4bytes

print('\n' + decoded_string)

# print('extra info: ' + str(len(decoded_string)) + decoded_string[258200:len(decoded_string)] + ' chars\n' )
t = open("C:/IT/onion_puzzle/layer2_response.txt", 'w')
t.write(decoded_string)  # how to put special characters to file ?
t.close()
# See PyCharm help at https://www.jetbrains.com/help/pycharm/



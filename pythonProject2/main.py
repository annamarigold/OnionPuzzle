

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


class IpHeader:
    def __init__(self, ip_version,
ip_header_size,
ip_first_byte,
ip_packet_size,
ip_id,
ip_frag_flag,
ip_ttl,
ip_udp_iana,
ip_header_checksum,
ip_sender,
ip_receiver):
      self.ip_version = ip_version
      self.ip_header_size = ip_header_size
      self.ip_first_byte = ip_first_byte
      self.ip_packet_size = ip_packet_size
      self.ip_id = ip_id
      self.ip_frag_flag = ip_frag_flag
      self.ip_ttl = ip_ttl
      self.ip_udp_iana = ip_udp_iana
      self.ip_header_checksum = ip_header_checksum
      self.ip_sender = ip_sender
      self.ip_receiver = ip_receiver

    def __str__(self):
        return f"{self.ip_version}{self.ip_header_size}{self.ip_first_byte}{self.ip_packet_size}{self.ip_id}{self.ip_frag_flag}{self.ip_ttl}{self.ip_udp_iana}{self.ip_header_checksum}{self.ip_sender}{self.ip_receiver}"


class Packet:
    def __init__(self, ip_header, udp_header, packet_data, valid):
        self.ip_header = ip_header
        self.udp_header = udp_header
        self.packet_data = packet_data
        self.valid = valid


def string_to_ip_header(string):
    ip_version = string[0:4]
    ip_header_size = string[4:8]
    ip_first_byte = string[8:16]
    ip_packet_size = string[16:32]
    ip_id = string[32:48]
    ip_frag_flag = string[48:64]
    ip_ttl = string[64:72]
    ip_udp_iana = string[72:80]
    ip_header_checksum = string [80:96]
    ip_sender = string[96:128]
    ip_receiver = string[128:160]
    ip_header = IpHeader(ip_version,
                         ip_header_size,
                         ip_first_byte,
                         ip_packet_size,
                         ip_id,
                         ip_frag_flag,
                         ip_ttl,
                         ip_udp_iana,
                         ip_header_checksum,
                         ip_sender,
                         ip_receiver)
    return ip_header


def ip_header_description():
    ip_version = '0100'#const
    ip_header_size = '0101'#const
    ip_first_byte = '00000000'#no need
    ip_packet_size = '0000000000011100'#min_size
    ip_id='0000000000000000'#no need
    ip_frag_flag='0000000000000000'#no fragmentation no need
    ip_ttl='00000000'#no need
    ip_udp_iana = '00010001' #UDP = 17
    ip_header_checksum = '0000000000000000' #always correct no need
    ip_sender = '00001010000000010000000100001010' #10.1.1.10
    ip_receiver = '00001010000000010000000111001000'#10.1.1.200
    ip_header_ref = IpHeader(ip_version,
                    ip_header_size,
                    ip_first_byte,
                    ip_packet_size,
                    ip_id,
                    ip_frag_flag,
                    ip_ttl,
                    ip_udp_iana,
                    ip_header_checksum,
                    ip_sender,
                    ip_receiver)
    return ip_header_ref


def ip_header_mask():
    ip_version = '1111'#const
    ip_header_size = '1111'#const
    ip_first_byte = '00000000'#no need
    ip_packet_size = '1111111111111111'#valuable info
    ip_id='0000000000000000'#no need
    ip_frag_flag='0000000000000000'#no fragmentation no need
    ip_ttl='00000000'#no need
    ip_udp_iana = '11111111' #UDP = 17
    ip_header_checksum = '0000000000000000' #always correct in this task no need
    ip_sender = '11111111111111111111111111111111' #10.1.1.10
    ip_receiver = '11111111111111111111111111111111'#10.1.1.200
    mask = (ip_version + ip_header_size + ip_first_byte +
              ip_packet_size + ip_id + ip_frag_flag + ip_ttl +
              ip_udp_iana + ip_header_checksum + ip_sender + ip_receiver)
    return mask


def check_ip_header(ip_header):
    ref = ip_header_description()
    if ref.ip_version == ip_header.ip_version:
        if ref.ip_header_size == ip_header.ip_header_size:
            if ref.ip_udp_iana == ip_header.ip_udp_iana:
                if ref.ip_sender == ip_header.ip_sender:
                    if ref.ip_packet_size <= ip_header.ip_packet_size:
                        return True
    return False


class UdpHeader:
    def __init__(self, port_sender, port_receiver, packet_size, checksum):
        self.port_sender = port_sender
        self.port_receiver = port_receiver
        self.packet_size = packet_size
        self.checksum = checksum

    def __str__(self):
        return f"{self.port_sender}{self.port_receiver}{self.packet_size}{self.checksum}"


def string_to_udp_header(string):
    port_sender = string[0:16]
    port_receiver = string[16:32]
    packet_size = string[32:48]
    checksum = string[48:64]
    upd_header = UdpHeader(port_sender, port_receiver, packet_size, checksum)
    return upd_header


def udp_header_description():
    port_sender = '0000000000000000'  # any port in this task
    port_receiver = '1010010001010101'  # 42069
    packet_size = '1111111111111111'  # min 8 byte max 65535 bytes for data+ip_header+udp+header
    checksum = '0000000000000000'  # always correct in this task no need
    upd_header = UdpHeader(port_sender, port_receiver, packet_size, checksum)
    return upd_header


def check_udp_header(udp_header):
    ref = udp_header_description()
    if ref.port_receiver == udp_header.port_receiver:
        if ref.packet_size >= '0000000001000000':
            return True
    return False


def udp_header_mask():
    port_sender = '0000000000000000' #any port in this task
    port_receiver = '1111111111111111' #42069
    packet_size = '1111111111111111' # min 8 byte max 65535 bytes for data+ip_header+udp+header
    checksum = '0000000000000000' #always correct in this task no need
    mask = (port_sender + port_receiver + packet_size + checksum)
    return mask


def first_compl_sum (string):
    summ = int('0000000000000000', 2)
    for z in range(0, len(string), 16):
        a = string[z:z+16]
        while len(a) < 16:
            a = a + '0'
        b = int(a, 2)
        summ = summ + b
    while summ > int('1111111111111111', 2):
        byte_str = format(summ, '032b')
        high_byte_str = byte_str[0:16]
        low_byte_str = byte_str[16:32]
        summ = int(high_byte_str, 2) + int(low_byte_str, 2)
    return summ


def udp_checksum(udp_header, ip_header, udp_data):
    if int(udp_header.packet_size, 2) % 2 == 1:
        udp_data = udp_data + '0'
        
    ip_pseudoheader = (ip_header.ip_sender + ip_header.ip_receiver +
                       '00000000' + '00010001' + udp_header.packet_size)
    
    udp_checksum = udp_header.checksum
    ip_checksum = ip_header.ip_header_checksum
    
    ip_header.ip_header_checksum = '0000000000000000'
    udp_header.checksum = '0000000000000000'
    
    ip_header_str = ip_header.__str__()
    ip_sum_calc = first_compl_sum(ip_header_str)
    ip_sum_calc = ~ip_sum_calc & 0xFFFF
    
    message = ip_pseudoheader + udp_header.__str__() + udp_data
    udp_sum_calc = first_compl_sum(message)
    udp_sum_calc = ~udp_sum_calc & 0xFFFF

    # print(format(udp_summ, '016b') + ' ' + udp_checksum)
    # print(ip_checksum + ' ' + format(ip_sum_calc, '016b'))

    if format(udp_sum_calc, '016b') == udp_checksum and ip_checksum == format(ip_sum_calc, '016b'):
        return True
    return False


def get_packet(datagramma):
    ip_header = string_to_ip_header(datagramma[0:160])
    udp_header = string_to_udp_header(datagramma[160:224])
    packet = Packet(datagramma[0:160], datagramma[160:224], '', False)

    # tmp = 'false'
    # if ip_header.ip_packet_size == udp_header.packet_size:
    #     tmp = 'true'
    # print(format(int(ip_header.ip_packet_size, 2)) + ' ' + format(int(udp_header.packet_size, 2)))

    if check_ip_header(ip_header):
        b = int(ip_header.ip_packet_size, 2) - 28
        data = datagramma[224:224+(b*8)]
        if check_udp_header(udp_header):
            if int(udp_header.packet_size, 2) + 20 == int(ip_header.ip_packet_size, 2):
                packet.valid = udp_checksum(udp_header, ip_header, data)
        data = encode_str(data, 5)
        packet.packet_data = data
    return packet


def layer5_main():
    f = open("C:/IT/OnionPuzzle/files/layer5.txt", "r")
    message = f.read()
    f.close()
    decoded_string = ''

    for x in range(0, len(message), 5):
        ch = message[x:x + 5]
        decoded_4bytes = decode_5_symbols(ch, 5)
        decoded_string = decoded_string + decoded_4bytes

    t = open("C:/IT/OnionPuzzle/files/layer5_middle_response.txt", 'w', encoding="utf-8")
    t.write(decoded_string)
    t.close()

    result = ''
    i = 0
    while i < len(decoded_string):
        datagramma = decoded_string[i:len(decoded_string)]
        temp = get_packet(datagramma)
        if temp.valid:
            result = result + temp.packet_data
        i = i + (len(temp.packet_data)*8 + len(temp.ip_header) + len(temp.udp_header))
    t = open("C:/IT/OnionPuzzle/files/layer5_response.txt", 'w', encoding="utf-8")
    t.write(result)
    t.close()

# layer1_main()
# layer2_main()
# layer3_main()
# layer4_main()
layer5_main()

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

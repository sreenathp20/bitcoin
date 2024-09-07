from bin_op import *


def sha256():
    text = 'oh my god i need to hack sha256! can i do it?9999999999'
    text = 'GILGRA2255407466'
    #text = "'01000010100010100010111110011000','01110001001101110100010010010001','10110101110000001111101111001111','11101001101101011101101110100101',"

    bin_in = ''.join(format(ord(i), '08b') for i in text)
    BLOCK_SIZE = 512
    length = len(bin_in) + 1 + 64

    blocks = (length//BLOCK_SIZE) + 1
    num_zeros = (BLOCK_SIZE*blocks) - length
    zeros = '0'*num_zeros
    message_block = bin_in+'1'+zeros+bin(len(bin_in))[2:].zfill(64)

    message_schedule = []
    for i in range(blocks):
        start = i*BLOCK_SIZE
        end = start + BLOCK_SIZE
        chunk = message_block[start:end]
        words = {}
        for j in range(16):
            word_size = 32
            start = j*word_size
            end = start+word_size
            word = chunk[start:end]
            words[j] = word    
        for j in range(16,64):
            w0 = words[j-16]
            w1 = words[j-15]
            w9 = words[j-7]
            w14 = words[j-2]
            w1R7 = rightRotate(w1,7)
            w1R18 = rightRotate(w1,18)
            w1RS3 = righ_shift(w1,3)
            x1 = XOR(w1R7,w1R18)
            sigma0 = XOR(x1,w1RS3)
            #sigma0 = XOR3(w1R7,w1R18,w1RS3)
            w14R17 = rightRotate(w14,17)
            w14R19 = rightRotate(w14,19)
            w14RS10 = righ_shift(w14,10)
            x1 = XOR(w14R17,w14R19)
            sigma1 = XOR(x1,w14RS10)
            #sigma1 = XOR3(w14R17,w14R19,w14RS10)
            x1 = add_binary_nums(w0,sigma0)
            x2 = add_binary_nums(x1,w9)
            wOut = add_binary_nums(x2,sigma1)
            words[j] = wOut
        message_schedule.append(words)

    initial_hash = {
        "h0": "01101010000010011110011001100111",
        "h1": "10111011011001111010111010000101",
        "h2": "00111100011011101111001101110010",
        "h3": "10100101010011111111010100111010",
        "h4": "01010001000011100101001001111111",
        "h5": "10011011000001010110100010001100",
        "h6": "00011111100000111101100110101011",
        "h7": "01011011111000001100110100011001"
    }

    k = ['01000010100010100010111110011000','01110001001101110100010010010001','10110101110000001111101111001111','11101001101101011101101110100101',   
                    '00111001010101101100001001011011','01011001111100010001000111110001','10010010001111111000001010100100','10101011000111000101111011010101',
                    '11011000000001111010101010011000','00010010100000110101101100000001','00100100001100011000010110111110','01010101000011000111110111000011',
                    '01110010101111100101110101110100','10000000110111101011000111111110','10011011110111000000011010100111','11000001100110111111000101110100',
                    '11100100100110110110100111000001','11101111101111100100011110000110','00001111110000011001110111000110','00100100000011001010000111001100',
                    '00101101111010010010110001101111','01001010011101001000010010101010','01011100101100001010100111011100','01110110111110011000100011011010',
                    '10011000001111100101000101010010','10101000001100011100011001101101','10110000000000110010011111001000','10111111010110010111111111000111',
                    '11000110111000000000101111110011','11010101101001111001000101000111','00000110110010100110001101010001','00010100001010010010100101100111',
                    '00100111101101110000101010000101','00101110000110110010000100111000','01001101001011000110110111111100','01010011001110000000110100010011',
                    '01100101000010100111001101010100','01110110011010100000101010111011','10000001110000101100100100101110','10010010011100100010110010000101',
                    '10100010101111111110100010100001','10101000000110100110011001001011','11000010010010111000101101110000','11000111011011000101000110100011',
                    '11010001100100101110100000011001','11010110100110010000011000100100','11110100000011100011010110000101','00010000011010101010000001110000',
                    '00011001101001001100000100010110','00011110001101110110110000001000','00100111010010000111011101001100','00110100101100001011110010110101',
                    '00111001000111000000110010110011','01001110110110001010101001001010','01011011100111001100101001001111','01101000001011100110111111110011',
                    '01110100100011111000001011101110','01111000101001010110001101101111','10000100110010000111100000010100','10001100110001110000001000001000',
                    '10010000101111101111111111111010','10100100010100000110110011101011','10111110111110011010001111110111','11000110011100010111100011110010']


    a = initial_hash['h0']
    b = initial_hash['h1']
    c = initial_hash['h2']
    d = initial_hash['h3']
    e = initial_hash['h4']
    f = initial_hash['h5']
    g = initial_hash['h6']
    h = initial_hash['h7']
    for i in range(blocks):    
        message_schedule[i]['wv'] = {}
        for j in range(64):
            wv = {'a': '', 'b': '', 'c': '', 'd': '', 'e': '', 'f': '', 'g': '', 'h': ''}
            if j == 0 and i > 0:
                last_wv = message_schedule[i-1]['wv'][64]
            if j > 0:
                last_wv = message_schedule[i]['wv'][j-1]
            a = a if j == 0 and i == 0 else last_wv['a']
            b = b if j == 0 and i == 0 else last_wv['b']
            c = c if j == 0 and i == 0 else last_wv['c']
            d = d if j == 0 and i == 0 else last_wv['d']
            e = e if j == 0 and i == 0 else last_wv['e']
            f = f if j == 0 and i == 0 else last_wv['f']
            g = g if j == 0 and i == 0 else last_wv['g']
            h = h if j == 0 and i == 0 else last_wv['h']
            eR6 = rightRotate(e,6)
            eR11 = rightRotate(e,11)
            eR25 = rightRotate(e,25)
            x1 = XOR(eR6,eR11)
            SIGMA1 = XOR(x1,eR25)
            choice = getChoice(e,f,g)
            x1 = add_binary_nums(h,SIGMA1)
            x2 = add_binary_nums(x1,choice)
            x3 = add_binary_nums(x2,k[j])
            temp1 = add_binary_nums(x3,message_schedule[i][j])
            aR2 = rightRotate(a,2)
            aR13 = rightRotate(a,13)
            aR22 = rightRotate(a,22)
            x1 = XOR(aR2,aR13)
            SIGMA0 = XOR(x1,aR22)
            aANDb = AND(a,b)
            aANDc = AND(a,c)
            bANDc = AND(b,c)
            x1 = XOR(aANDb, aANDc)
            majority = XOR(x1,bANDc)
            temp2 = add_binary_nums(SIGMA0,majority)
            wv['h'] = g 
            wv['g'] = f 
            wv['f'] = e
            wv['e'] = add_binary_nums(d,temp1)
            wv['d'] = c 
            wv['c'] = b 
            wv['b'] = a 
            wv['a'] = add_binary_nums(temp1,temp2)
            wv['temp1'] = temp1
            wv['temp2'] = temp2
            wv['SIGMA1'] = SIGMA1
            wv['choice'] = choice
            wv['SIGMA0'] = SIGMA0
            wv['majority'] = majority
            s12scomplement = twosComplement(SIGMA1)
            choice2scomplement = twosComplement(choice)
            k2scomplement = twosComplement(k[j])
            x1 = add_binary_nums(temp1,s12scomplement)
            x2 = add_binary_nums(x1,choice2scomplement)
            t1_s1_ch_k = add_binary_nums(x2, k2scomplement)
            wv['t1_s1_ch_k'] = t1_s1_ch_k
            message_schedule[i]['wv'][j] = wv
        res = wv
        if i == 0:
            init_hash = initial_hash
            A = add_binary_nums(res['a'],init_hash['h0'])
            B = add_binary_nums(res['b'],init_hash['h1'])
            C = add_binary_nums(res['c'],init_hash['h2'])
            D = add_binary_nums(res['d'],init_hash['h3'])
            E = add_binary_nums(res['e'],init_hash['h4'])
            F = add_binary_nums(res['f'],init_hash['h5'])
            G = add_binary_nums(res['g'],init_hash['h6'])
            H = add_binary_nums(res['h'],init_hash['h7'])
            
        else:
            init_hash = message_schedule[i-1]['wv'][64]
            A = add_binary_nums(res['a'],init_hash['a'])
            B = add_binary_nums(res['b'],init_hash['b'])
            C = add_binary_nums(res['c'],init_hash['c'])
            D = add_binary_nums(res['d'],init_hash['d'])
            E = add_binary_nums(res['e'],init_hash['e'])
            F = add_binary_nums(res['f'],init_hash['f'])
            G = add_binary_nums(res['g'],init_hash['g'])
            H = add_binary_nums(res['h'],init_hash['h'])
        message_schedule[i]['initial_hash'] = init_hash
        result = {'a': A, 'b': B, 'c': C, 'd': D, 'e': E, 'f': F, 'g': G, 'h': H}
        message_schedule[i]['wv'][64] = result

    binary = A+B+C+D+E+F+G+H
    message_schedule.append({})
    message_schedule[blocks]['sha256_binary'] = binary
    sha256 = hex(int(binary, 2))[2:].zfill(64)
    message_schedule[blocks]['sha256'] = sha256
    message_schedule[blocks]['input'] = text
    message_schedule[blocks]['input_binary'] = bin_in
    message_schedule[blocks]['message_block'] = message_block
    message_schedule[blocks]['K'] = k
    
    print("sha256: ",sha256)
    import hashlib
    result = hashlib.sha256(text.encode()).hexdigest()
    print("result: ", result)
    print("Valid:", equality(sha256, result))
    return message_schedule
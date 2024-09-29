from bin_op import *

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

K = ['01000010100010100010111110011000','01110001001101110100010010010001','10110101110000001111101111001111','11101001101101011101101110100101',   
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

def reverseSha256():
    sha256 = '335edfa039f04f073d10b2d1718874e4268dd3704580f15e542ef9fcb833d06f'
    binary = bin(int(sha256, 16))[2:].zfill(256)
    message = {}
    wv = []
    for i in range(0,256,32):
        wv.append(binary[i:i+32])
    message['result']=wv
    ikeys = list(initial_hash.keys())
    wv = []
    for i in range(8):
        ini = initial_hash[ikeys[i]]
        ini2scomplement = twosComplement(ini)
        wv.append(add_binary_nums(message['result'][i], ini2scomplement))
    message['63']=wv

    a_63,b_63,c_63,d_63,e_63,f_63,g_63,h_63 = wv[0],wv[1],wv[2],wv[3],wv[4],wv[5],wv[6],wv[7]

    a_62 = b_63
    b_62 = c_63
    c_62 = d_63
    e_62 = f_63
    f_62 = g_63
    g_62 = h_63
    
    
    # e_63 = d_62 + temp1
    # d_62 = e_63 - temp1
    # a_63 = temp1 + temp2
    # temp1 = a_63 - temp2 
    # temp2 = Σ0 + Majority
    aR2 = rightRotate(a_62,2)
    aR13 = rightRotate(a_62,13)
    aR22 = rightRotate(a_62,22)
    x1 = XOR(aR2,aR13)
    SIGMA0 = XOR(x1,aR22)
    aANDb = AND(a_62,b_62)
    aANDc = AND(a_62,c_62)
    bANDc = AND(b_62,c_62)
    x1 = XOR(aANDb, aANDc)
    majority = XOR(x1,bANDc)
    temp2 = add_binary_nums(SIGMA0,majority)
    temp22scomplement = twosComplement(temp2)
    temp1 = add_binary_nums(a_63, temp22scomplement)
    temp12scomplement = twosComplement(temp1)
    d_62 = add_binary_nums(e_63,temp12scomplement)
    wv = [a_62, b_62, c_62, d_62, e_62, f_62, g_62, '']
    message['62']=wv

    a_61 = b_62
    b_61 = c_62
    c_61 = d_62
    e_61 = f_62
    f_61 = g_62    
    aR2 = rightRotate(a_61,2)
    aR13 = rightRotate(a_61,13)
    aR22 = rightRotate(a_61,22)
    x1 = XOR(aR2,aR13)
    SIGMA0 = XOR(x1,aR22)
    aANDb = AND(a_61,b_61)
    aANDc = AND(a_61,c_61)
    bANDc = AND(b_61,c_61)
    x1 = XOR(aANDb, aANDc)
    majority = XOR(x1,bANDc)
    temp2 = add_binary_nums(SIGMA0,majority)
    temp22scomplement = twosComplement(temp2)
    temp1 = add_binary_nums(a_62, temp22scomplement)
    temp12scomplement = twosComplement(temp1)
    d_61 = add_binary_nums(e_62,temp12scomplement)
    wv = [a_61, b_61, c_61, d_61, e_61, f_61, '', '']
    message['61']=wv


    a_60 = b_61
    b_60 = c_61
    c_60 = d_61
    e_60 = f_61
    aR2 = rightRotate(a_60,2)
    aR13 = rightRotate(a_60,13)
    aR22 = rightRotate(a_60,22)
    x1 = XOR(aR2,aR13)
    SIGMA0 = XOR(x1,aR22)
    aANDb = AND(a_60,b_60)
    aANDc = AND(a_60,c_60)
    bANDc = AND(b_60,c_60)
    x1 = XOR(aANDb, aANDc)
    majority = XOR(x1,bANDc)
    temp2 = add_binary_nums(SIGMA0,majority)
    temp22scomplement = twosComplement(temp2)
    temp1 = add_binary_nums(a_61, temp22scomplement)
    temp12scomplement = twosComplement(temp1)
    d_60 = add_binary_nums(e_61,temp12scomplement)
    wv = [a_60, b_60, c_60, d_60, e_60, '', '', '']
    message['60']=wv


    a_59 = b_60
    b_59 = c_60
    c_59 = d_60
    aR2 = rightRotate(a_59,2)
    aR13 = rightRotate(a_59,13)
    aR22 = rightRotate(a_59,22)
    x1 = XOR(aR2,aR13)
    SIGMA0 = XOR(x1,aR22)
    aANDb = AND(a_59,b_59)
    aANDc = AND(a_59,c_59)
    bANDc = AND(b_59,c_59)
    x1 = XOR(aANDb, aANDc)
    majority = XOR(x1,bANDc)
    temp2 = add_binary_nums(SIGMA0,majority)
    temp22scomplement = twosComplement(temp2)
    temp1 = add_binary_nums(a_60, temp22scomplement)
    temp12scomplement = twosComplement(temp1)
    d_59 = add_binary_nums(e_60,temp12scomplement)

    wv = [a_59, b_59, c_59, d_59, '', '', '', '']
    message['59']=wv
    pass


reverseSha256()

from .test_blockminer import *
import codecs
import time


def rightRotate(n, st):
    return st[len(st) - n:]+st[:len(st)-n]

def righShift(n,st):
    return '0'*n+st[:len(st)-n]

def xor(st1, st2):
    if len(st1) != len(st2):
        print("Error xor")
        return None
    st3 = ''
    for i in range(len(st1)):
        # print(i)
        # print(len(st2))
        if st1[i] == '0' and st2[i] == '0':
            st3 += '0'
        if st1[i] == '1' and st2[i] == '1':
            st3 += '0'
        if st1[i] == '0' and st2[i] == '1':
            st3 += '1'
        if st1[i] == '1' and st2[i] == '0':
            st3 += '1'
    return st3

def binaryToDecimal(n):
    return int(n,2)

def add(st1, st2):
    num1 = binaryToDecimal(st1)
    num2 = binaryToDecimal(st2)
    res = num1+num2
    b = bin(res)[2:]
    ex = len(b) - len(st1)
    if ex > 0:
        return b[ex:]
    else:
        ex = -ex
        return (ex * '0')+b
    
def bAnd(b1, b2):
    d1 = binaryToDecimal(b1)
    d2 = binaryToDecimal(b2)
    d3 = d1 & d2
    b = bin(d3)[2:]
    res = (32-len(b))*'0'+b
    return res

def bNOT(b):
    b2 = ''
    for i in range(len(b)):
        if b[i] == '0':
            b2 += '1'
        if b[i] == '1':
            b2 += '0'
    return b2

def binToHexa(n):
   
    # convert binary to int
    num = int(n, 2)
     
    # convert int to hexadecimal
    hex_num = hex(num)
    hex_num = hex_num[2:]
    hex_num = (8 - len(hex_num)) * '0'+hex_num
    return(hex_num)

def hexToBin(h):
    b = bin(int(h, 16))[2:]
    res = (4-len(b))*'0'+b
    return res

def littleEndian(string):
    splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
    splited.reverse()
    return "".join(splited)


            



def getNonce(nonce):
    hex_nonce = hex(nonce)[2:]
    #print("hex_nonce:", hex_nonce, " ", len(hex_nonce))
    n = 2
    hex_nonce_field4 = (8-len(hex_nonce))*'0'+hex_nonce
    #print("hex_nonce_field4:", hex_nonce_field4, " ", len(hex_nonce_field4))
    hex_nonce_arr = [hex_nonce_field4[i:i+n] for i in range(0, len(hex_nonce_field4), n)]
    nonce_hex_swap = "".join(hex_nonce_arr[::-1])
    return nonce_hex_swap

def process2(block_header):
    result = []

    s = block_header

    for none_i in range(1):
        # nonce = getNonce(none_i)
        # if none_i % 100 == 0:
        #     print("none_i:", none_i)    
        #     print("nonce:", nonce)
        # s = block_header+nonce
        bin_block_header = "".join([hexToBin(i) for i in s])
        # print("nonce:", nonce, " ", len(nonce))
        # print("block_header:", block_header, " ", len(block_header))
        # print("s:", s, " ", len(s))        

        for indx in range(2):
            result.append({})
            
            bin_block_header = "".join([hexToBin(c) for c in s])
            print("s                :", s, " ", len(s))  
            print("bin_block_header :", bin_block_header, " ", len(bin_block_header))
            cnt =len(bin_block_header)
            result[indx]["s"] = s
            result[indx]["bin_block_header"] = bin_block_header
            ucnt = cnt + 1

            #print("ucnt:", ucnt)

            md = 512 - 64

            zcnt = (512 - ((ucnt+64)%512))
            #print("zcnt:", zcnt)
            zeros = zcnt*'0'

            #print("zeros:",zeros)

            #mb = ''.join(lbs)+'1'+zeros
            mb = bin_block_header+'1'+zeros
            #print("mb:",len(mb))

            len_zeros = (64-len(bin(cnt)[2:]))*'0'

            len_block = len_zeros+bin(cnt)[2:]

            #print(len(len_block))

            message_block = mb+len_block

            result[indx]["message_block"] = message_block

            #print("len(message_block):",len(message_block))

            #print(len(message_block) % 512)

            l = len(message_block) // 512
            w = {}
            for i in range(l):
                w[i] = []
                print("block "+str(i+1))
                st = i*512
                end = st+512
                block = message_block[st:end]
                b = 512 // 32
                for idx in range(b):
                    st = idx * 32
                    w[i].append(block[st:st+32])
                    print(block[st:st+8], " ", block[st+8:st+16], " ", block[st+16:st+24], " ", block[st+24:st+32])




            #print("Words")

            hexa = ['6a09e667',
                'bb67ae85',
                '3c6ef372',
                'a54ff53a',
                '510e527f',
                '9b05688c',
                '1f83d9ab',
                '5be0cd19']

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

            hb = [ bin(int(i,16))[2:] for i in hexa]

            hb = [ ((32-len(i))*'0')+i for i in hb]

            h0 = hb[0]
            h1 = hb[1]
            h2 = hb[2]
            h3 = hb[3]
            h4 = hb[4]
            h5 = hb[5]
            h6 = hb[6]
            h7 = hb[7]
            #print("hb:", hb)
            a = hb[0]
            b = hb[1]
            c = hb[2]
            d = hb[3]
            e = hb[4]
            f = hb[5]
            g = hb[6]
            h = hb[7]

            words = w
            for key in words.keys():
                #print("===============================")
                i = 0
                for w0 in words[key]:
                    #print(str(i)+"  :",w0)
                    i += 1
                w = words[key]
                for i in range(16,64):
                    w0 = w[i-16] 
                    w9 = w[i-7]
                    w1 = w[i-15]
                    w14 = w[i-2]
                    rr7 = rightRotate(7,w1)
                    rr18 = rightRotate(18,w1)
                    rs3 = righShift(3,w1)
                    sigma0 = xor( xor(rr7, rr18), rs3)
                    #print("w14   :",w14)
                    rr17 = rightRotate(17,w14)
                    rr19 = rightRotate(19, w14)
                    rs10 = righShift(10, w14)
                    #print("rr17  :",rr17)
                    #print("rr19  :",rr19)
                    t1 = xor(rr17, rr19)
                    #print("t1    :",t1)
                    #print("rs10  :",rs10)
                    sigma1 = xor( t1, rs10)
                    #print("sigma1:", sigma1)
                    t1 = add( w0, sigma0 )
                    t2 = add( t1, w9)
                    # w16 = w0 + σ0 + w9 + σ1
                    w16 = add( t2, sigma1)
                    w.append(w16)
                    #print(str(i)+"    :",w16)
                for i in range(len(k)):
                    #Temp1 = h + Σ1 + Choice + k0 + w0   
                    #Temp2 = Σ0 + Majority
                    # Σ1 =(e rightrotate 6) xor
                    #     (e rightrotate 11) xor
                    #     (e rightrotate 25)
                    eRR6 = rightRotate(6,e)
                    eRR11 = rightRotate(11, e)
                    eRR25 = rightRotate(25, e)
                    SIGMA1 = xor( xor( eRR6, eRR11 ), eRR25)
                    #Choice = (e and f) xor ((not e) and g)
                    eandf = bAnd(e, f)
                    notE = bNOT(e)
                    notEandG = bAnd(notE, g)
                    # print("e         :",e, " ", len(e))
                    # print("notE      :",notE, " ", len(notE))
                    # print("f         :",f, " ", len(f))
                    # print("g         :",g, " ", len(g))
                    choice = xor(eandf, notEandG)
                    aRR2 = rightRotate(2, a)
                    aRR13 = rightRotate(13,a)
                    aRR22 = rightRotate(22,a)
                    # Σ0 =(a rightrotate 2) xor
                    #     (a rightrotate 13) xor
                    #     (a rightrotate 22)
                    SIGMA0 = xor( xor( aRR2,aRR13 ), aRR22)    
                    #Majority = (a and b) xor (a and c) xor (b and c)
                    aANDb = bAnd(a,b)
                    aANDc = bAnd(a,c)
                    bANDc = bAnd(b,c)
                    majority = xor( xor( aANDb, aANDc ), bANDc)
                    temp1 = add( add( add( add(h,SIGMA1), choice), k[i]), w[i])
                    #print("h         :",h, " ", len(h))
                    # print("SIGMA1    :",SIGMA1, " ", len(SIGMA1))
                    # print("choice    :",choice, " ", len(choice))
                    # print("k[i]      :",k[i], " ", len(k[i]))
                    # print("w[i]      :",w[i], " ", len(w[i]))
                    #print("temp1     :",temp1, " ", len(temp1))
                    #Temp2 = Σ0 + Majority
                    temp2 = add( SIGMA0, majority )
                    # print("SIGMA0    :",SIGMA0, " ", len(SIGMA0))
                    # print("majority  :",majority, " ", len(majority))
                    #print("temp2     :",temp2, " ", len(temp2))
                    temp1plustemp2 = add( temp1, temp2 )
                    #print("temp1plustemp2     :",temp1plustemp2, " ", len(temp1plustemp2))
                    dplustemp1 = add( d, temp1 )
                    #print("dplustemp1     :",dplustemp1, " ", len(dplustemp1))
                    h = g
                    g = f
                    f = e
                    e = dplustemp1
                    d = c
                    c = b
                    b = a
                    a = temp1plustemp2

                # print("a :",a)
                # print("h0:",h0)

                h0 = add( a, h0 )
                h1 = add( b, h1 )
                h2 = add( c, h2 )
                h3 = add( d, h3 )
                h4 = add( e, h4 )
                h5 = add( f, h5 )
                h6 = add( g, h6 )
                h7 = add( h, h7 )

                a = h0
                b = h1
                c = h2
                d = h3
                e = h4
                f = h5
                g = h6
                h = h7

                # print("h0:",h0)
                # print("h1:",h1)
                # print("h2:",h2)
                # print("h3:",h3)
                # print("h4:",h4)
                # print("h5:",h5)
                # print("h6:",h6)
                # print("h7:",h7)




            # w16 = w0 + σ0 + w9 + σ1

            # where

            # σ0 =
            # (w1 rightrotate 7) xor
            # (w1 rightrotate 18) xor
            # (w1 rightshift 3)
            # and

            # σ1 =
            # (w14 rightrotate 17) xor
            # (w14 rightrotate 19) xor
            # (w14 rightshift 10)

            # rs = '0111'
            # rs = '0111'
            # rr7_temp = rs[len(rs)-7:]+rs[:len(rs)-7]
            # rr7 = rightRotate(7,rs)
            # rr18 = rightRotate(18,rs)
            # rs3 = righShift(3,rs)
            # print("word     :",rs)
            # print("word rr7 :", rr7)
            # print("word rr18:", rr18)
            # print("word rs3 :", rs3)
            # t1 = xor(rr7,rr18)
            # sigma0 = xor(t1, rs3)
            #print("sigma0   :",sigma0)
            #print(add(rs,rs))

            #print(binaryToDecimal(rs))

                


            # import math
            # sq = math.sqrt(2)
            # fr = str(sq).split(".")[1]
            # print("fr:", fr)
            # print('{:032b}'.format(int(fr)))
            # bn = bin(int( fr ))[2:]
            # print(bn[len(bn)-32:])







            h0 = binToHexa(h0)
            h1 = binToHexa(h1)
            h2 = binToHexa(h2)
            h3 = binToHexa(h3)
            h4 = binToHexa(h4)
            h5 = binToHexa(h5)
            h6 = binToHexa(h6)
            h7 = binToHexa(h7)
            res = h0+h1+h2+h3+h4+h5+h6+h7
            #print("res:", res, " ", len(res))
            import hashlib
            #m = hashlib.sha256(s.encode('UTF-8'))
            #print(m.hexdigest())
            # if res == m.hexdigest():
            #     print("True")
            # else:
            #     print("False")

            result[indx]["out"] = res

            s = res

        

            
        out = littleEndian(s)
        result.append({"out": out})
        print("out: ", out)
        return result

def getBits(hash):   
    #hash = "00000000000000000002393cd1853041010241871caedc6f8307588d49d8b1c5"
    hash, block_hedaer, version, previousblockhash, merkleroot, time, bits, nonce, height = checkData(hash)
    res = process2(block_hedaer)
    return block_hedaer, version, previousblockhash, merkleroot, time, bits, nonce, res, height
    #time.sleep(5)
#block_header, target = bm.getBlockHeader()
#block_header, target = bm.mineBlockHeader()
#block_header, target = bm.mineBlockHeaderReverse()
#exit()


#exit()









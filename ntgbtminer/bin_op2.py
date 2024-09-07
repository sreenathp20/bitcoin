from bin_op import *


out = {}

out["sha256"] = "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855"
out["res"] = {
    "h0": "01100101100000101101100101110110",
    "h1": "00101101101010111001010011001001",
    "h2": "01000001110000100010011010111010",
    "h3": "00010010110011011101001111101011",
    "h4": "01100101110111110001011011110010",
    "h5": "10101010010010111100010011001110",
    "h6": "01011001100011111010101100001101",
    "h7": "00011100001001100000111000001010"
}
out["initial"] = {
    "h0": "01101010000010011110011001100111",
    "h1": "10111011011001111010111010000101",
    "h2": "00111100011011101111001101110010",
    "h3": "10100101010011111111010100111010",
    "h4": "01010001000011100101001001111111",
    "h5": "10011011000001010110100010001100",
    "h6": "00011111100000111101100110101011",
    "h7": "01011011111000001100110100011001"
}

wv = {
    "a":"", "b": "", "c": "", "d": "", "e": "", "f": "", "g": "", "h": ""
}
out[64] = wv.copy()
wv_keys = list(wv.keys())
i = 0
for key in out["res"].keys():
    res = out["res"]
    init = out["initial"]
    h2scomplement = twosComplement(init[key])
    val = add_binary_nums(res[key], h2scomplement)
    out[64][wv_keys[i]] = val[-32:]
    i += 1
pass

for i in range(63, -1, -1):
    out[i] = wv.copy()
    out[i]['a'] = out[i+1]['b']
    out[i]['b'] = out[i+1]['c']
    out[i]['c'] = out[i+1]['d']
    out[i]['e'] = out[i+1]['f']
    out[i]['f'] = out[i+1]['g']
    out[i]['g'] = out[i+1]['h']
    a = out[i]['a']
    b = out[i]['b']
    c = out[i]['c']
    e = out[i]['e']
    f = out[i]['f']
    g = out[i]['g']
    next_a = out[i+1]['a']
    next_e = out[i+1]['e']
    aR2 = rightRotate(a,2)
    aR13 = rightRotate(a,13)
    aR22 = rightRotate(a,22)
    SIGMA0 = XOR3(aR2,aR13,aR22)
    aANDb = AND(a,b)
    aANDc = AND(a,c)
    bANDc = AND(b,c)
    majority = XOR3(aANDb,aANDc,bANDc)
    temp2 = add_binary_nums(SIGMA0,majority)
    temp22scomplement = twosComplement(temp2)
    temp1 = add_binary_nums(next_a,temp22scomplement)[-32:]
    temp12scomplement = twosComplement(temp1)[-32:]
    d = add_binary_nums(next_e,temp12scomplement)[-32:]
    out[i]['d'] = d
    k63 = '11000110011100010111100011110010'
    # Temp1 = h + Σ1 + Choice + k63 + w63
    # h + w63 = Temp1 - Σ1 - Choice - k63
    # next_a = Temp1 + Temp2
    # next_a = h + Σ1 + Choice + k63 + w63 + Temp2
    # h + w63 = next_a - Σ1 - Choice - k63 - Temp2
    eR6 = rightRotate(e,6)
    eR11 = rightRotate(e,11)
    eR25 = rightRotate(e,25)
    SIGMA1 = XOR3(eR6,eR11,eR25)
    # eANDf = AND(e,f)
    # eNOT= onesComplement(e)
    # eNOTANDg = AND(eNOT,g)
    # choice = XOR(eANDf,eNOTANDg)
    choice = getChoice(e,f,g)
    SIGMA12scomplement = twosComplement(SIGMA1)
    choice2scomplement = twosComplement(choice)
    k632scomplement = twosComplement(k63)
    x1 = add_binary_nums(temp1,SIGMA12scomplement)
    x2 = add_binary_nums(x1,choice2scomplement)
    hplusw63 = add_binary_nums(x2,k632scomplement)
    pass




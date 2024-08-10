# ntgbtminer - vsergeev - https://github.com/vsergeev/ntgbtminer
#
# No Thrils GetBlockTemplate Bitcoin Miner
#
# This is mostly a demonstration of the GBT protocol.
# It mines at a measly 550 KH/s on my computer, but
# with a whole lot of spirit ;)
#
import codecs
import urllib.request
import urllib.error
import urllib.parse
import base64
import json
import hashlib
import struct
import random
import time
import os
import sys
from db import MongoDb
import random



# JSON-HTTP RPC Configuration
# This will be particular to your local ~/.bitcoin/bitcoin.conf

RPC_URL = os.environ.get("RPC_URL", "http://127.0.0.1:8332")
RPC_USER = os.environ.get("RPC_USER", "admin")
RPC_PASS = os.environ.get("RPC_PASS", "admin")

################################################################################
# Bitcoin Daemon JSON-HTTP RPC
################################################################################


def rpc(method, params=None):
    """
    Make an RPC call to the Bitcoin Daemon JSON-HTTP server.

    Arguments:
        method (string): RPC method
        params: RPC arguments

    Returns:
        object: RPC response result.
    """
    try:
        print("RPC_URL:", RPC_URL)
        print("RPC_USER:", RPC_USER)
        print("RPC_PASS:", RPC_PASS)
        rpc_id = random.getrandbits(32)
        data = json.dumps({"id": rpc_id, "method": method, "params": params}).encode()
        auth = base64.encodebytes((RPC_USER + ":" + RPC_PASS).encode()).decode().strip()

        request = urllib.request.Request(RPC_URL, data, {"Authorization": "Basic {:s}".format(auth)})
        with urllib.request.urlopen(request) as f:
            response = json.loads(f.read())
    except:
        return rpc(method, params)

    if response['id'] != rpc_id:
        raise ValueError("Invalid response id: got {}, expected {:u}".format(response['id'], rpc_id))
    elif response['error'] is not None:
        raise ValueError("RPC error: {:s}".format(json.dumps(response['error'])))

    return response['result']

################################################################################
# Bitcoin Daemon RPC Call Wrappers
################################################################################

# def rpc_getblocktemplate():
#     out = os.popen("bitcoin-cli getblocktemplate '{\"rules\": [\"segwit\"]}'").read()
#     #print("out:", out)
#     json_out = json.loads(out)
#     #print("height:", json_out['height'])
#     return json_out

def rpc_getblocktemplate():
    try:
        m = MongoDb()
        data = m.read("test_blocktemplate", {})
        if len(data) > 0:
            return data[0]
        out = rpc("getblocktemplate", [{"rules": ["segwit"]}])
        #out["_id"] = 1        
        in_data = [out]
        m = MongoDb()
        #m.insertMany("test_blocktemplate", in_data)
        return out
    except ValueError:
        return {}

def rpc_getmininginfo():
    try:  
        out = os.popen("bitcoin-cli -rpcuser="+RPC_USER+" -rpcpassword="+RPC_PASS+" getmininginfo").read()
        #print("out:", out)
        json_out = json.loads(out)
    except:
        return rpc_getmininginfo()
    return json_out


# def rpc_submitblock(block_submission, block_hash):
#     print("bitcoin-cli submitblock \""+block_hash+"\"")
#     out = os.popen("bitcoin-cli submitblock \""+block_hash+"\"").read()
#     print("out:", out)
#     json_out = json.loads(out)
    #return rpc("submitblock", [block_submission])

def rpc_submitblock(block_submission, block_hash):
    return rpc("submitblock", [block_submission])


################################################################################
# Representation Conversion Utility Functions
################################################################################


def int2lehex(value, width):
    """
    Convert an unsigned integer to a little endian ASCII hex string.

    Args:
        value (int): value
        width (int): byte width

    Returns:
        string: ASCII hex string
    """

    return value.to_bytes(width, byteorder='little').hex()


def int2varinthex(value):
    """
    Convert an unsigned integer to little endian varint ASCII hex string.

    Args:
        value (int): value

    Returns:
        string: ASCII hex string
    """

    if value < 0xfd:
        return int2lehex(value, 1)
    elif value <= 0xffff:
        return "fd" + int2lehex(value, 2)
    elif value <= 0xffffffff:
        return "fe" + int2lehex(value, 4)
    else:
        return "ff" + int2lehex(value, 8)


def bitcoinaddress2hash160(addr):
    """
    Convert a Base58 Bitcoin address to its Hash-160 ASCII hex string.

    Args:
        addr (string): Base58 Bitcoin address

    Returns:
        string: Hash-160 ASCII hex string
    """

    table = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"

    hash160 = 0
    addr = addr[::-1]
    for i, c in enumerate(addr):
        hash160 += (58 ** i) * table.find(c)

    # Convert number to 50-byte ASCII Hex string
    hash160 = "{:050x}".format(hash160)

    # Discard 1-byte network byte at beginning and 4-byte checksum at the end
    return hash160[2:50 - 8]


################################################################################
# Transaction Coinbase and Hashing Functions
################################################################################


def tx_encode_coinbase_height(height):
    """
    Encode the coinbase height, as per BIP 34:
    https://github.com/bitcoin/bips/blob/master/bip-0034.mediawiki

    Arguments:
        height (int): height of the mined block

    Returns:
        string: encoded height as an ASCII hex string
    """

    width = (height.bit_length() + 7) // 8

    return bytes([width]).hex() + int2lehex(height, width)


def tx_make_coinbase(coinbase_script, address, value, height):
    """
    Create a coinbase transaction.

    Arguments:
        coinbase_script (string): arbitrary script as an ASCII hex string
        address (string): Base58 Bitcoin address
        value (int): coinbase value
        height (int): mined block height

    Returns:
        string: coinbase transaction as an ASCII hex string
    """

    # See https://en.bitcoin.it/wiki/Transaction

    coinbase_script = tx_encode_coinbase_height(height) + coinbase_script

    # Create a pubkey script
    # OP_DUP OP_HASH160 <len to push> <pubkey> OP_EQUALVERIFY OP_CHECKSIG
    pubkey_script = "76" + "a9" + "14" + bitcoinaddress2hash160(address) + "88" + "ac"

    tx = ""
    # version
    tx += "01000000"
    # in-counter
    tx += "01"
    # input[0] prev hash
    tx += "0" * 64
    # input[0] prev seqnum
    tx += "ffffffff"
    # input[0] script len
    tx += int2varinthex(len(coinbase_script) // 2)
    # input[0] script
    tx += coinbase_script
    # input[0] seqnum
    tx += "ffffffff"
    # out-counter
    tx += "01"
    # output[0] value
    tx += int2lehex(value, 8)
    # output[0] script len
    tx += int2varinthex(len(pubkey_script) // 2)
    # output[0] script
    tx += pubkey_script
    # lock-time
    tx += "00000000"

    return tx


def tx_compute_hash(tx):
    """
    Compute the SHA256 double hash of a transaction.

    Arguments:
        tx (string): transaction data as an ASCII hex string

    Return:
        string: transaction hash as an ASCII hex string
    """

    return hashlib.sha256(hashlib.sha256(bytes.fromhex(tx)).digest()).digest()[::-1].hex()


def tx_compute_merkle_root(tx_hashes):
    """
    Compute the Merkle Root of a list of transaction hashes.

    Arguments:
        tx_hashes (list): list of transaction hashes as ASCII hex strings

    Returns:
        string: merkle root as a big endian ASCII hex string
    """

    # Convert list of ASCII hex transaction hashes into bytes
    tx_hashes = [bytes.fromhex(tx_hash)[::-1] for tx_hash in tx_hashes]

    # Iteratively compute the merkle root hash
    while len(tx_hashes) > 1:
        # Duplicate last hash if the list is odd
        if len(tx_hashes) % 2 != 0:
            tx_hashes.append(tx_hashes[-1])

        tx_hashes_new = []

        for i in range(len(tx_hashes) // 2):
            # Concatenate the next two
            concat = tx_hashes.pop(0) + tx_hashes.pop(0)
            # Hash them
            concat_hash = hashlib.sha256(hashlib.sha256(concat).digest()).digest()
            # Add them to our working list
            tx_hashes_new.append(concat_hash)

        tx_hashes = tx_hashes_new

    # Format the root in big endian ascii hex
    return tx_hashes[0][::-1].hex()


################################################################################
# Block Preparation Functions
################################################################################

def getVersion(version):
    hex_version = hex(version)[2:]
    n = 2
    hex_version_arr = [hex_version[i:i+n] for i in range(0, len(hex_version), n)]
    #print("version hex:", hex_version)
    version_hex_swap = "".join(hex_version_arr[::-1])
    return version_hex_swap

def getPreviousblockhash(previousblockhash):
    n = 2
    previousblockhash_swap = "".join( [ previousblockhash[i:i+n] for i in range(0, len(previousblockhash), n) ][::-1] )
    return previousblockhash_swap

def getMerkleroot(merkleroot):
    n = 2
    merkleroot_swap = "".join( [ merkleroot[i:i+n] for i in range(0, len(merkleroot), n) ][::-1] )
    return merkleroot_swap

def getTime(t):
    hex_t = hex(t)[2:]
    n = 2
    hex_t_arr = [hex_t[i:i+n] for i in range(0, len(hex_t), n)]
    t_hex_swap = "".join(hex_t_arr[::-1])
    return t_hex_swap

def getBits(bits):
    bits = str(bits)
    print("type of bits:", type(bits))
    n = 2
    bits_swap = "".join( [ bits[i:i+n] for i in range(0, len(bits), n) ][::-1] )
    return bits_swap

def getNonce(nonce):
    hex_nonce = hex(nonce)[2:]
    #print("hex_nonce:", hex_nonce, " ", len(hex_nonce))
    n = 2
    hex_nonce_field4 = (8-len(hex_nonce))*'0'+hex_nonce
    #print("hex_nonce_field4:", hex_nonce_field4, " ", len(hex_nonce_field4))
    hex_nonce_arr = [hex_nonce_field4[i:i+n] for i in range(0, len(hex_nonce_field4), n)]
    nonce_hex_swap = "".join(hex_nonce_arr[::-1])
    return nonce_hex_swap

def littleEndian(string):
    splited = [str(string)[i:i + 2] for i in range(0, len(str(string)), 2)]
    splited.reverse()
    return "".join(splited)

def mineBlockHeader():
    m = MongoDb()
    data = m.read("test_blocktemplate", {})
    block = data[0]
    version = getVersion(block["version"])
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["curtime"])
    print("bits:", len(block["bits"]))
    bits = getBits(block["bits"])
    #nonce = getNonce(block["nonce"])
    nonce = getNonce(896554680)
    #print("nonce:", nonce)
    block_header = version+previousblockhash+merkleroot+time+bits#+nonce
    target = block['target']
    print("block_header:", block_header)
    low = 'f'*64
    mod = 10000
    for none_i in range(4294967295):
        nonce = getNonce(none_i)
        if none_i % mod == 0:
            print("none_i:", none_i)    
            print("nonce:", nonce)
            print("low:", low)
            print("diff :", int(low, 16) - int(target, 16) )
        block_header = block_header+nonce
        header_hex = (block_header)
        header_bin = codecs.decode(header_hex, 'hex')                   #First decode string data to real hex value
        #print("header_bin:", header_bin)
        hash = hashlib.sha256(header_bin).digest()                                                    #Calculate the first hash 
        #print ("First Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

        #First Hash =>  d20176bc6e0b0a904efdfe257b8a50143cd6e3d4f2a154460d7d3a770b9847c4

        hash = hashlib.sha256(hash).digest()                                      #Calculate second hash on the first hash
        #print ("Second Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

        #Second Hash =>  bf0e2e13fce62f3a5f15903a177ad6a258a01f164aefed7d4a03000000000000

        hash = codecs.encode(hash, 'hex_codec').decode('ascii')          #Convert data back to the string value

        out = littleEndian(hash)

        #print("out:", out)
        if out < low:
            low = out
            print("============================================================")
            print("low changed")
            print("low out:", out)
        if out < target:
            print("Block mined! ", nonce)
            print("out! ", out)
            print("True")
            exit()
        else:
            if none_i % mod == 0:
                print("out! ", out)
                print("False")

def mineBlockHeaderReverse():
    m = MongoDb()
    data = m.read("test_blocktemplate", {})
    block = data[0]
    version = getVersion(block["version"])
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["curtime"])
    print("bits:", len(block["bits"]))
    bits = getBits(block["bits"])
    #nonce = getNonce(block["nonce"])
    nonce = getNonce(896554680)
    #print("nonce:", nonce)
    block_header = version+previousblockhash+merkleroot+time+bits#+nonce
    target = block['target']
    print("block_header:", block_header)
    low = 'f'*64
    mod = 10000
    for none_i in range(4294967295, 2000000000, -1):
        nonce = getNonce(none_i)
        if none_i % mod == 0:
            print("none_i:", none_i)    
            print("nonce:", nonce)
            print("low:", low)
            print("diff :", int(low, 16) - int(target, 16) )
        block_header = block_header+nonce
        header_hex = (block_header)
        header_bin = codecs.decode(header_hex, 'hex')                   #First decode string data to real hex value
        #print("header_bin:", header_bin)
        hash = hashlib.sha256(header_bin).digest()                                                    #Calculate the first hash 
        #print ("First Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

        #First Hash =>  d20176bc6e0b0a904efdfe257b8a50143cd6e3d4f2a154460d7d3a770b9847c4

        hash = hashlib.sha256(hash).digest()                                      #Calculate second hash on the first hash
        #print ("Second Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

        #Second Hash =>  bf0e2e13fce62f3a5f15903a177ad6a258a01f164aefed7d4a03000000000000

        hash = codecs.encode(hash, 'hex_codec').decode('ascii')          #Convert data back to the string value

        out = littleEndian(hash)

        #print("out:", out)
        if out < low:
            low = out
            print("============================================================")
            print("low changed")
            print("low out:", out)
        if out < target:
            print("Block mined! ", nonce)
            print("out! ", out)
            print("True")
            exit()
        else:
            if none_i % mod == 0:
                print("out! ", out)
                print("False")

def getBlockHeader():
    m = MongoDb()
    data = m.read("test_blocktemplate", {})
    block = data[0]
    version = getVersion(block["version"])
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["curtime"])
    print("bits:", len(block["bits"]))
    bits = getBits(block["bits"])
    #nonce = getNonce(block["nonce"])
    nonce = getNonce(896554680)
    print("nonce:", nonce)
    block_header = version+previousblockhash+merkleroot+time+bits#+nonce
    print("block_header:", block_header)
    return block_header, block['target']


def checkData(get_hash):

    m = MongoDb()
    data = m.read("blocks", {"hash":get_hash})
    #print("data:",data)
    block = data[0]
    height = block["height"]
    get_hash = block["previousblockhash"]
    hash = block["hash"]
    version = getVersion(block["version"])    
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["time"])
    
    bits = getBits(block["bits"])
    nonce = getNonce(block["nonce"])
    #nonce = getNonce(896554680)
    print("version          :", version, " ", len(version))
    print("previousblockhash:", previousblockhash, " ", len(previousblockhash))
    print("merkleroot       :", merkleroot, " ", len(merkleroot))
    print("time             :", time, " ", len(time))
    print("bits             :", bits, " ", len(bits))
    print("nonce            :", nonce, " ", len(nonce))
    block_header = version+previousblockhash+merkleroot+time+bits+nonce
    print("block_header     :", block_header, " ", len(block_header))
    # hash = hashlib.sha256(hashlib.sha256(block_header.encode()).digest()).hexdigest()[::-1]
    # hash1 = hashlib.sha256(block_header.encode()).hexdigest()
    #print("hash:", hash)
    #print("hash1:", hash1)

    #print("len(block['tx']:",len(block['tx']))

    #merkleroot = tx_compute_merkle_root([tx for tx in block['tx']])
    #print("merkleroot       :", merkleroot)  

    
    
    # scale = 16 ## equals to hexadecimal
    # num_of_bits = 8
    # bin_block_header = bin(int(block_header, scale))[2:]
    # print("bin_block_header :", bin_block_header, " ", len(bin_block_header))

    header_hex = (block_header)

    header_bin = codecs.decode(block_header, 'hex')                 #First decode string data to real hex value
    #print("header_bin       :", header_bin, " ", len(header_bin))
    hash = hashlib.sha256(header_bin).digest()                                                    #Calculate the first hash 
    #print ("First Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

    #First Hash =>  d20176bc6e0b0a904efdfe257b8a50143cd6e3d4f2a154460d7d3a770b9847c4

    hash = hashlib.sha256(hash).digest()                                      #Calculate second hash on the first hash
    #print ("Second Hash => ", codecs.encode(hash, 'hex_codec').decode('ascii'))

    #Second Hash =>  bf0e2e13fce62f3a5f15903a177ad6a258a01f164aefed7d4a03000000000000

    hash = codecs.encode(hash, 'hex_codec').decode('ascii')          #Convert data back to the string value

    out = littleEndian(hash)

    print("out              :", out)

    print("hash             :", block["hash"])

    if out == block["hash"]:
        print("True")
    else:
        print("False")
    return get_hash, block_header, height

def checkData2(height):

    m = MongoDb()
    data = m.read("blocks", {"height":height})
    #print("data:",data)
    block = data[0]
    height = block["height"]
    get_hash = block["previousblockhash"]
    hash1 = block["hash"]
    version = getVersion(block["version"])    
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["time"])
    
    bits = getBits(block["bits"])
    nonce = getNonce(block["nonce"])
    #nonce = getNonce(896554680)
    print("version          :", version, " ", len(version))
    print("previousblockhash:", previousblockhash, " ", len(previousblockhash))
    print("merkleroot       :", merkleroot, " ", len(merkleroot))
    print("time             :", time, " ", len(time))
    print("bits             :", bits, " ", len(bits))
    print("nonce            :", nonce, " ", len(nonce))
    block_header = version+previousblockhash+merkleroot+time+bits+nonce
    print("block_header     :", block_header, " ", len(block_header))

    header_hex = (block_header)
    return get_hash, block_header, height, hash1

def checkData3(block):
    height = block["height"]
    get_hash = block["previousblockhash"]
    hash1 = block["hash"]
    version = getVersion(block["version"])    
    previousblockhash = getPreviousblockhash(block["previousblockhash"])
    merkleroot = getMerkleroot(block["merkleroot"])
    time = getTime(block["time"])
    
    bits = getBits(block["bits"])
    nonce = getNonce(block["nonce"])
    #nonce = getNonce(896554680)
    print("version          :", version, " ", len(version))
    print("previousblockhash:", previousblockhash, " ", len(previousblockhash))
    print("merkleroot       :", merkleroot, " ", len(merkleroot))
    print("time             :", time, " ", len(time))
    print("bits             :", bits, " ", len(bits))
    print("nonce            :", nonce, " ", len(nonce))
    block_header = version+previousblockhash+merkleroot+time+bits+nonce
    print("block_header     :", block_header, " ", len(block_header))

    header_hex = (block_header)
    return get_hash, block_header, height, hash1


def block_make_header_new(block):
    header = ""
    header += hex(block['version'])

def block_make_header(block):
    """
    Make the block header.

    Arguments:
        block (dict): block template

    Returns:
        bytes: block header
    """

    header = b""

    # Version
    header += struct.pack("<L", block['version'])
    # Previous Block Hash
    header += bytes.fromhex(block['previousblockhash'])[::-1]
    # Merkle Root Hash
    # print("block['merkleroot']:", block['merkleroot'])
    # print("block['merkleroot'][::-1]:", block['merkleroot'][::-1])
    # print("bytes.fromhex(block['merkleroot'])[0]:", bytes.fromhex(block['merkleroot'])[0:4])
    # print("bytes.fromhex(block['merkleroot'])[::-1]:", bytes.fromhex(block['merkleroot'])[::-1])

    header += bytes.fromhex(block['merkleroot'])[::-1]
    # Time
    header += struct.pack("<L", block['curtime'])
    # Target Bits
    header += bytes.fromhex(block['bits'])[::-1]
    # Nonce
    header += struct.pack("<L", block['nonce'])
    #print("header: ", header)
    return header

def insertToDb(height, block_hash, target_hash, nonce, extranonce):
    data = {
        "height": height,
        "block_hash": block_hash,
        "target_hash": target_hash,
        "nonce": nonce,
        "extranonce": extranonce
    }
    m = MongoDb()
    m.insertMany("mined_blocks", [data])
    pass


def block_compute_raw_hash(header):
    """
    Compute the raw SHA256 double hash of a block header.

    Arguments:
        header (bytes): block header

    Returns:
        bytes: block hash
    """

    return hashlib.sha256(hashlib.sha256(header).digest()).digest()[::-1]


def block_bits2target(bits):
    """
    Convert compressed target (block bits) encoding to target value.

    Arguments:
        bits (string): compressed target as an ASCII hex string

    Returns:
        bytes: big endian target
    """

    # Bits: 1b0404cb
    #       1b          left shift of (0x1b - 3) bytes
    #         0404cb    value
    bits = bytes.fromhex(bits)
    shift = bits[0] - 3
    value = bits[1:]

    # Shift value to the left by shift
    target = value + b"\x00" * shift
    # Add leading zeros
    target = b"\x00" * (32 - len(target)) + target

    return target


def block_make_submit(block):
    """
    Format a solved block into the ASCII hex submit format.

    Arguments:
        block (dict): block template with 'nonce' and 'hash' populated

    Returns:
        string: block submission as an ASCII hex string
    """

    submission = ""

    # Block header
    submission += block_make_header(block).hex()
    # Number of transactions as a varint
    submission += int2varinthex(len(block['transactions']))
    # Concatenated transactions data
    for tx in block['transactions']:
        submission += tx['data']

    return submission


################################################################################
# Block Miner
################################################################################


def block_mine(block_template, coinbase_message, extranonce_start, address, timeout=None, debugnonce_start=False):
    """
    Mine a block.

    Arguments:
        block_template (dict): block template
        coinbase_message (bytes): binary string for coinbase script
        extranonce_start (int): extranonce offset for coinbase script
        address (string): Base58 Bitcoin address for block reward

    Timeout:
        timeout (float): timeout in seconds
        debugnonce_start (int): nonce start for testing purposes

    Returns:
        (block submission, hash rate) on success,
        (None, hash rate) on timeout or nonce exhaustion.
    """
    # Add an empty coinbase transaction to the block template transactions
    coinbase_tx = {}
    print("block_template['transactions']:", block_template['transactions'][0])
    block_template['transactions'].insert(0, coinbase_tx)
    print("block_template['transactions']:", block_template['transactions'][0])
    height = block_template['height']

    # Add a nonce initialized to zero to the block template
    block_template['nonce'] = 0

    # Compute the target hash
    target_hash = block_bits2target(block_template['bits'])

    # Mark our mine start time
    time_start = time.time()

    # Initialize our running average of hashes per second
    hash_rate, hash_rate_count = 0.0, 0

    # Loop through the extranonce
    #extranonce = extranonce_start
    extranonce = random.randrange(1,0xffffffff)
    while extranonce <= 0xffffffff:
        # Update the coinbase transaction with the new extra nonce
        coinbase_script = coinbase_message + int2lehex(extranonce, 4)
        coinbase_tx['data'] = tx_make_coinbase(coinbase_script, address, block_template['coinbasevalue'], block_template['height'])
        coinbase_tx['hash'] = tx_compute_hash(coinbase_tx['data'])
        coinbase_tx['txid'] = coinbase_tx['hash']
        # print("coinbase_tx:", coinbase_tx)
        # break
        # print("block_template['transactions'][0]:", block_template['transactions'][0])
        # Recompute the merkle root
        block_template['merkleroot'] = tx_compute_merkle_root([tx['txid'] for tx in block_template['transactions']])
        #print("merkleroot:", block_template['merkleroot'])
        #break
        # Reform the block header
        #print("block_template:", block_template)
        #print("block_template['transactions']:", block_template['transactions'][0])
        #exit()
        m = MongoDb()
        in_data = [block_template]
        m.delete("test_blocktemplate", {})
        m = MongoDb()
        m.insertMany("test_blocktemplate", in_data)
        block_header = block_make_header(block_template)

        m = MongoDb()
        #data = m.read("test_block_header", {})
        # print("block_header      :",block_header)
        # print("block_header[0:76]:",block_header[0:76])
        
        #if len(data) == 0:
        in_data = [{"data": block_header}]
        m.insertMany("test_block_header", in_data)

        # new_block_template = rpc_getblocktemplate()

        # new_height = new_block_template['height']
        # if height != new_height:
        #     return (None, None, None)

        time_stamp = time.time()

        # Loop through the nonce
        nonce = 0 if not debugnonce_start else debugnonce_start
        while nonce <= 0xffffffff:
            # Update the block header with the new 32-bit nonce
            block_header = block_header[0:76] + nonce.to_bytes(4, byteorder='little')
            #print("block_header :",block_header)
            # Recompute the block hash
            block_hash = block_compute_raw_hash(block_header)
            #print("block_hash   :",block_hash.hex())
            if nonce % 1000000 == 0:
                print(nonce, " ", block_hash.hex(), " ", target_hash.hex())
                pass
            if nonce % 5000000 == 0:
                mininginfo = rpc_getmininginfo()

                new_height = int(mininginfo['blocks']) + 1
                
                if height != new_height:
                    m = MongoDb()
                    data = m.read("test_blocktemplate", {})
                    if len(data) > 0:
                        d = data[0]
                        if d['height'] == height:
                            m = MongoDb()
                            m.delete("test_blocktemplate", {})
                    print("new_height: ", new_height)
                    return (None, None, None)

            
            # if nonce > 2:
            #     time.sleep(5)
            # Check if it the block meets the target hash
            if block_hash < target_hash:
                block_template['nonce'] = nonce
                block_template['hash'] = block_hash.hex()
                insertToDb(height, block_hash.hex(), target_hash.hex(), nonce, extranonce)
                return (block_template, hash_rate, block_hash.hex())

            # Measure hash rate and check timeout
            if nonce > 0 and nonce % 1048576 == 0:
                hash_rate = hash_rate + ((1048576 / (time.time() - time_stamp)) - hash_rate) / (hash_rate_count + 1)
                hash_rate_count += 1

                time_stamp = time.time()

                # If our mine time expired, return none
                if timeout and (time_stamp - time_start) > timeout:
                    return (None, hash_rate)

            nonce += 1
        extranonce += 1

    # If we ran out of extra nonces, return none
    return (None, hash_rate)


################################################################################
# Standalone Bitcoin Miner, Single-threaded
################################################################################


def standalone_miner(coinbase_message, address, debugnonce_start):
    while True:
        block_template = rpc_getblocktemplate()
        #print("block_template:", block_template)

        mined_block = None

        while not mined_block:
            block_template = rpc_getblocktemplate()
            print("debugnonce_start: ", debugnonce_start)
            print("Mining block template, height {:d}...".format(block_template['height']))
            #def block_mine(block_template, coinbase_message, extranonce_start, address, timeout=None, debugnonce_start=False):
            mined_block, hash_rate, block_hash = block_mine(block_template, coinbase_message, 0, address, None, debugnonce_start)
            if hash_rate:
                print("    {:.4f} KH/s\n".format(hash_rate / 1000.0))

        if mined_block:
            print("Solved a block! Block hash: {}".format(mined_block['hash']))
            submission = block_make_submit(mined_block)

            #print("Submitting:", submission, "\n")
            response = rpc_submitblock(submission, block_hash)
            if response is not None:
                print("Submission Error: {}".format(response))
                break


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Usage: {:s} <coinbase message> <block reward address>".format(sys.argv[0]))
        sys.exit(1)

    standalone_miner(sys.argv[1].encode().hex(), sys.argv[2], int(sys.argv[3]) )

import os
import ecdsa
import binascii
import hashlib
import base58

def bytes_to_hex_string(b: bytes):
    return ''.join('{:02x}'.format(x) for x in b).upper()

def get_prepend_if_even_or_odd_for_compressed(x_point):
    y = int(x_point[64:], 16)
    if y % 1 == 1:
        return "03"  # odd
    return "02"  # even

private_key = binascii.hexlify(os.urandom(32)).decode()
#private_key = ""
              
print("private_key :", private_key)
private_key = bytes.fromhex(private_key)



sk = ecdsa.SigningKey.from_string(private_key, curve=ecdsa.SECP256k1)

#print("sk:", sk)

vk = sk.get_verifying_key()

#print("vk:", vk)

msg = "hello world"

#print("msg.encode():", msg.encode())

signed_msg = sk.sign(msg.encode())

#print("signed_msg:",  binascii.hexlify(signed_msg).decode())

assert vk.verify(signed_msg, "hello world".encode())

x_point = bytes_to_hex_string(vk.to_string())
#print(f"Uncompressed private key (hex):\t\t 04{x_point.upper()}")

even_odd = get_prepend_if_even_or_odd_for_compressed(x_point)

public_key = bytes.fromhex(even_odd) + vk.to_string()[:32]


#print(vk.to_string())
#print("vk.to_string()[:32] :", vk.to_string()[:32])

#public_key = ("04" + vk.to_string())

print("public_key: ", binascii.hexlify(public_key).decode())

sha256_1 = hashlib.sha256(public_key)

ripemd160 = hashlib.new("ripemd160")
ripemd160.update(sha256_1.digest())

hashed_public_key = bytes.fromhex("00") + ripemd160.digest()

#print("hashed_public_key: ", hashed_public_key)

checksum_full = hashlib.sha256(
    hashlib.sha256(hashed_public_key).digest()).digest()

checksum = checksum_full[:4]

bin_addr = hashed_public_key + checksum

address = str(base58.b58encode(bin_addr))

print("address:", address)

final_address = address[2:-1]

print("final_address:", final_address)

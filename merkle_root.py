import hashlib
import json
import os


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

height = 697227
hash = "000000000000000000039e86c9bd0731c676b329f2540241e8f340d2a34acfd2"

out = os.popen("bitcoin-cli getblock "+hash).read()

json_out = json.loads(out)

#print(json_out['tx'])

print(tx_compute_merkle_root(json_out['tx']))

    


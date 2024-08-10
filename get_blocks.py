import os
import json
from db import MongoDb
import time


height = 808299
hash = "00000000000000000001e3fef608c2c411d48177e729aa4d2dae1609abce36bf"



while height > 0:
    m = MongoDb()
    out = os.popen("bitcoin-cli -rpcuser=admin --rpcpassword=admin getblock "+hash).read()
    try:
        json_out = json.loads(out)
        height = json_out['height']
        hash = json_out['nextblockhash']
        #height = -1
        print(json_out['hash'])
        print(json_out['height'])
        #print(json_out.keys())
        #print('previousblockhash', json_out['previousblockhash'])
        #print('height', json_out['height'])
        data = [{
            'height': json_out['height'],
            'hash': json_out['hash'],
            'confirmations': json_out['confirmations'],
            'version': json_out['version'],
            'versionHex': json_out['versionHex'],
            'merkleroot': json_out['merkleroot'],
            'time': json_out['time'],
            'mediantime': json_out['mediantime'],
            'nonce': json_out['nonce'],
            'bits': json_out['bits'],
            'difficulty': json_out['difficulty'],
            'chainwork': json_out['chainwork'],
            'nTx': json_out['nTx'],
            'previousblockhash': json_out['previousblockhash'] if 'previousblockhash' in json_out else None,
            'nextblockhash': json_out['nextblockhash'] if 'nextblockhash' in json_out else None,
            'strippedsize': json_out['strippedsize'],
            'size': json_out['size'],
            'weight': json_out['weight'],
            'tx': json_out['tx']
        }]
        m.insertMany('blocks', data)
    except:
        time.sleep(5)


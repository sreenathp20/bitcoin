import os
import json
from db import MongoDb


height = 412146
hash = "0000000000000000020c60bb18fd07fb322e600c12a1989bd3f014e2785cbad8"

m = MongoDb()

while height > 1:

    out = os.popen("bitcoin-cli -rpcuser sree -password admin getblock "+hash).read()

    json_out = json.loads(out)
    height = json_out['height']
    hash = json_out['previousblockhash']
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
        'tx_size': len(json_out['tx'])
    }]
    #m.insertMany('blocks', data)

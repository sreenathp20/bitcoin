import os
import json
import requests
from db import MongoDb


height = 412145
hash = "0000000000000000020c60bb18fd07fb322e600c12a1989bd3f014e2785cbad8"

m = MongoDb()

while height > 1:
    try:
        
        response = requests.get('https://blockchain.info/rawblock/'+hash)

        #response = requests.get('https://chain.api.btc.com/v3/block/'+str(height))
        # print(response.json()['data'].keys())
        print(response.json().keys())
        out = response.json()
        json_out = out
        height = json_out['height']
        hash = json_out['prev_block']
        #height = -1
        print(json_out['hash'])
        print(json_out['height'])
    except:
        print("error:", height)
        continue
    #print(json_out.keys())
    #print('previousblockhash', json_out['previousblockhash'])
    #print('height', json_out['height'])
    data = [{
        'height': json_out['height'],
        'hash': json_out['hash'],
        'confirmations': json_out['confirmations'] if 'confirmations' in json_out else None,
        'version': json_out['ver'],
        'versionHex': json_out['versionHex'] if 'versionHex' in json_out else None,
        'merkleroot': json_out['mrkl_root'],
        'time': json_out['time'],
        'mediantime': json_out['mediantime'] if 'mediantime' in json_out else None,
        'nonce': json_out['nonce'],
        'bits': json_out['bits'],
        'difficulty': json_out['difficulty'] if 'difficulty' in json_out else None,
        'chainwork': json_out['chainwork'] if 'chainwork' in json_out else None,
        'nTx': json_out['n_tx'],
        'previousblockhash': json_out['prev_block'] if 'prev_block' in json_out else None,
        'nextblockhash': json_out['next_block_hash'] if 'next_block_hash' in json_out else None,
        'strippedsize': json_out['strippedsize']  if 'strippedsize' in json_out else None,
        'size': json_out['size'],
        'weight': json_out['weight'] if 'weight' in json_out else None,
        'tx_size': len(json_out['tx'])
    }]
    #print(data)
    #height -= 1
    m.insertMany('blocks', data)
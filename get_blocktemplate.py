import os
import json

out = os.popen("bitcoin-cli getblocktemplate '{\"rules\": [\"segwit\"]}'").read()

json_out = json.loads(out)

print(json_out.keys())

print(json_out['transactions'][0])

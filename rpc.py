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

RPC_URL = os.environ.get("RPC_URL", "http://127.0.0.1:8332")
RPC_USER = os.environ.get("RPC_USER", "sree")
RPC_PASS = os.environ.get("RPC_PASS", "admin")

def rpc(method, params=None):
    """
    Make an RPC call to the Bitcoin Daemon JSON-HTTP server.

    Arguments:
        method (string): RPC method
        params: RPC arguments

    Returns:
        object: RPC response result.
    """
    print("RPC_URL:", RPC_URL)
    print("RPC_USER:", RPC_USER)
    print("RPC_PASS:", RPC_PASS)
    rpc_id = random.getrandbits(32)
    data = json.dumps({"id": rpc_id, "method": method, "params": params}).encode()
    auth = base64.encodebytes((RPC_USER + ":" + RPC_PASS).encode()).decode().strip()

    request = urllib.request.Request(RPC_URL, data, {"Authorization": "Basic {:s}".format(auth)})

    with urllib.request.urlopen(request) as f:
        response = json.loads(f.read())

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
        return rpc("getblockchaininfo")
    except ValueError:
        return {}
    
print(rpc_getblocktemplate())
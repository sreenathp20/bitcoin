from django.http import HttpResponse
from django.shortcuts import render
from .db import MongoDb
import json
import os
import random
import urllib.request
import urllib.error
import urllib.parse
import base64
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


RPC_URL = os.environ.get("RPC_URL", "http://127.0.0.1:8332")
RPC_USER = os.environ.get("RPC_USER", "admin")
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

    

def index(request):
    return HttpResponse('Hello, welcome to the index page.')

def user(request):
    return HttpResponse('Hi, this is where an individual post will be.')

def read_blocktemplate(request):
    try:
        m = MongoDb()
        data = m.read("blocktemplate", {})
        return JsonResponse(data, safe=False)
    except ValueError:
        return JsonResponse({}, safe=False)
    
def delete_blocktemplate(request):
    try:
        m = MongoDb()
        print("delete_blocktemplate")
        m.delete("blocktemplate", {})
        return JsonResponse({})
    except ValueError:
        return JsonResponse({})

def getblocktemplate(request):
    try:
        m = MongoDb()
        data = m.read("blocktemplate", {})
        if len(data) > 0:
            print("data:", len(data))
            #return JsonResponse({'foo':'bar'})
            if "_id" in data[0]:
                del data[0]["_id"]
            print("data[0]:", data[0].keys())
            return JsonResponse(data[0], safe=False)
        out = rpc("getblocktemplate", [{"rules": ["segwit"]}])
        #out["_id"] = 1        
        in_data = [out]
        m = MongoDb()
        m.insertMany("blocktemplate", in_data)
        if "_id" in out:
                del out["_id"]
        print("out:", out.keys())
        return JsonResponse(out, safe=False)
    except ValueError:
        return JsonResponse({}, safe=False)
    
def rpc_getmininginfo():    
    try:
        out = os.popen("bitcoin-cli -rpcuser="+RPC_USER+" -rpcpassword="+RPC_PASS+" getmininginfo").read()
        #print("out:", out)
        json_out = json.loads(out)
    except:
        return rpc_getmininginfo()
    return json_out
    
def getmininginfo(request):
    data = rpc_getmininginfo()
    return JsonResponse(data)

def insertToDb(data):
    m = MongoDb()
    m.insertMany("mined_blocks", [data])
    pass

@csrf_exempt
def mined_block(request):
    if request.method == 'POST':
        data = {
            "height": request.POST['height'],
            "block_hash": request.POST['block_hash'],
            "target_hash": request.POST['target_hash'],
            "nonce": request.POST['nonce'],
            "extranonce": request.POST['extranonce']
        }
        insertToDb(data)
        #print("request.POST:", request.POST)
    return JsonResponse({"msg": "success"}) 

@csrf_exempt
def submitblock(request):
    if request.method == 'POST':
        res = rpc("submitblock", [request.POST['submission']])
        #print("request.POST:", request.POST)
    return JsonResponse({"response": res})
    
import sys
import binascii
import os
import time
import shutil
from subprocess import call
import json

from Savoir import Savoir
import ipfsapi

def getSavoirOptions(chain_name):
    """ Return rpc_user, rpcpassword, rpchost, rpcport, and chain_name for the chain 'chain_name' """
    pathconf = "/root/.multichain/" + chainname + "/multichain.conf"
    rpcuser = ""
    rpcpassword = ""

    with open("/root/.multichain/chain1/multichain.conf", "r") as f:
        line_list = [c for c in f.readlines()]
        for line in line_list:
            if "rpcuser=" in line:
                rpcuser = line.split("=")[1]
            elif "rpcpassword=" in line:
                rpcpassword = line.split("=")[1]
        assert(rpcuser != "")
        assert(rpcpassword != "")

    rpcuser = rpcuser.replace('\n', '')
    rpcpassword = rpcpassword.replace('\n', '')

    rpchost = '127.0.0.1'
    rpcport = '1235'

    return rpcuser, rpcpassword, rpchost, rpcport, chain_name

def connectChain(ip, chain_name, nickname, port=1234):
    """ Connect to the chain at 'ip' address where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    apirpc = Savoir(getSavoirOptions(chain_name))
    api = ipfsapi.connect('127.0.0.1', 5001)
    apirpc.stop
    time.sleep(2)
    shutil.rmtree("/root/.multichain/" + str(chain_name))
    call("multichaind", str(chain_name) + "@" + str(ip) + ":" + str(port), "-daemon", "-autosubscribe=streams")
    call("ipfs", "daemon")
    time.sleep(2)
    json_myaddr = apirpc.getaddresses
    json_addr = apirpc.liststreamkeyitems("default_account", "address")
    json_priv = apirpc.liststreamkeyitems("default_account", "privkey")

    hex_addr = json.load(json_addr[0]['data'])
    hex_priv = json.load(json_priv[0]['data'])
    my_addr = json.load(json_myaddr[0])

    default_privkey = hex_priv.decode("hex")
    default_address = hex_addr.decode("hex")

    apirpc.importaddress(default_address)
    txid = apirpc.createrawsendfrom(default_address, '{"my_addr":0}')
    signed_hex_json = apirpc.signrawtransaction(txid, "null", "[" + str(default_privkey) + "]")
    signed_hex = json.load(signed_hex_json['hex'])
    apirpc.sendrawtransaction(signed_hex)

    print("Please wait...")
    time.sleep(20)

    hex_nick = nickname.encode("hex")
    apirpc.publish("nickname_resolve", "pseudo", str(hex_nick))

    print("---------- Terminé ------------")



def createChain(chain_name, nickname):
    """ Create a new chain where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    pass

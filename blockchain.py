import sys
import binascii
import os
import time
import shutil
from subprocess import call
import json
from Savoir import Savoir
import ipfsapi


def getSavoirOptions(chain_name, rpchost='127.0.0.1', rpcport='1235'):
    """ Return rpc_user, rpcpassword, rpchost, rpcport, and chain_name for the chain 'chain_name' """
    pathconf = "/root/.multichain/" + chain_name + "/multichain.conf"
    rpcuser = ""
    rpcpassword = ""

    with open(pathconf, "r") as f:
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

    return rpcuser, rpcpassword, rpchost, rpcport, chain_name


def connectChain(ip, chain_name, nickname, port='1234'):
    """ Connect to the chain at 'ip' address where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    apirpc = Savoir(getSavoirOptions(chain_name))
    apirpc.stop()
    time.sleep(2)
    shutil.rmtree("/root/.multichain/" + str(chain_name))
    call("multichaind", str(chain_name) + "@" + str(ip) + ":" + str(port), "-daemon", "-autosubscribe=streams")
    call("ipfs", "daemon")
    time.sleep(2)
    json_myaddr = apirpc.getaddresses()
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

    pubkey = json.load(apirpc.getaddresses("true")[0]['pubkey'])
    hex_nick = nickname.encode("hex")
    apirpc.publish("nickname_resolve", "nickname", str(hex_nick))
    apirpc.publish("nickname_resolve", "pubkey", pubkey)

    print("---------- Finished -----------")


def createChain(chain_name, nickname, port='1234', rpcport='1235'):
    """ Create a new chain where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    call("multichain-cli", chain_name, "stop")
    time.sleep(2)
    call("firewall-cmd", "--permanent", "--zone=public", "--add-port=" + port + "/tcp")
    call("systemctl", "restart", "firewalld.service")
    shutil.move("/root/.multichain/multichain.conf", "/root")
    shutil.rmtree("/root/.multichain/" + str(chain_name))
    shutil.move("/root//multichain.conf", "/root/.multichain/")
    call("multichain-util", "create", chain_name, "-default-network-port=" + port, "-default-rpc-port=" + rpc_port, "-anyone-can-connect=true", "-anyone-can-create=true", "-anyone-can-mine=true", "-anyone-can-receive=true")
    call("multichaind", chain_name, "-daemon", "autosubscribe=streams")
    call("ipfs", "daemon")

    time.sleep(5)

    apirpc = Savoir(getSavoirOptions(chain_name))
    api = ipfsapi.connect('127.0.0.1', 5001)

    json = apirpc.createkeypairs()
    address = json.load(json[0]['address'])
    pubkey = json.load(json[0]['pubkey'])
    privkey = json.load(json[0]['privkey'])

    apirpc.create("stream", "default_account", "false")
    apirpc.send(address, "0")

    hex_addr = address.encode("hex")
    hex_priv = privkey.encode("hex")

    time.sleep(2)

    apirpc.publish("default_account", "address", hex_addr)
    apirpc.publish("default_account", "pubkey", pubkey)
    apirpc.publish("default_account", "privkey", hex_priv)

    apirpc.create("stream", "nickname_resolve", "true")

    time.sleep(2)

    hex_nick = str(nickname).encode("hex")
    apirpc.publish("nickname_resolve", "nickname", hex_nick)
    apirpc.publish("nickname_resolve", "pubkey", pubkey)

    print("--------- Finished ----------")


def createGroup(chain_name, group_name, *users):
    """ Create a group in chain 'chain_name', with the name 'group_name' and composed with
    users *users.
    Ex usage: createGroup("chain1", "insa_group", "benoit", "vladimir", "rodolphe")"""
    apirpc = Savoir(getSavoirOptions(chain_name))
    api = ipfsapi.connect('127.0.0.1', 5001)
    streamname = binascii.hexlify("[Group]" + str(group_name))
    apirpc.create('stream', streamname, "False")

    for user in users:
        pass

def getPublicKey(nickname, apirpc):
    """ Return the public key of user 'nickname', None if user not found. """
    pass

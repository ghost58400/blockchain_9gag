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

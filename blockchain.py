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

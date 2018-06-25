import binascii
import os
import shutil
import time
from subprocess import call

from Savoir import Savoir
from consts import *
import ipfsapi


def get_chain_name():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/chain_name.txt', 'r')
    val = file.read()
    file.close()
    val = val.replace('\n', '')
    return val


def set_chain_name(name):
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/chain_name.txt', 'w')
    file.write(name)
    file.close()


def get_api(host=default_rpc_host, port=default_rpc_port, chain_name=''):
    if chain_name == '':
        chain_name = get_chain_name()
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
        if rpcuser == "":
            print("Couldn't retrieve rpcuser from " + chain_name)
            return None
        elif rpcpassword == "":
            print("Couldn't retrieve rpcpassword from " + chain_name)
            return None

    rpcuser = rpcuser.replace('\n', '')
    rpcpassword = rpcpassword.replace('\n', '')

    return Savoir(rpcuser, rpcpassword, host, port, chain_name)


def resolve_name(account, api):
    # ajouter prise en compte du plus recent, pour changement pseudo
    nicknames = api.liststreamitems('nickname_resolve')
    ret = 'name not found'
    for nickname in nicknames:
        if nickname['publishers'][0] == account:
            if nickname['key'] == 'pseudo':
                ret = binascii.unhexlify(nickname['data'])
    return ret


def get_all_posts(api):
    raw_stream_names = api.liststreams()
    streams = []
    for stream in raw_stream_names:
        if stream['name'] != 'root' and stream['name'] != 'default_account' and stream['name'] != 'nickname_resolve':
            streams.append(stream['name'])

    posts = []
    for stream in streams:
        stream = api.liststreamitems(stream)
        nom = binascii.unhexlify(stream)
        ipfs = ''
        type_contenu = ''
        author_account = ''
        for it in stream:
            if it['key'] == 'ipfs':
                ipfs = binascii.unhexlify(it['data'])
                author_account = it['publishers'][0]
            if it['key'] == 'type':
                type_contenu = binascii.unhexlify(it['data'])
        if ipfs != '' and type_contenu != '' and author_account != '':
            author = resolve_name(author_account, api)
            posts.append({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author})

    return posts


def connect_chain(ip, port, chain_name, nickname):
    # heavy stuff
    apirpc = get_api()
    apirpc.stop()
    time.sleep(2)
    shutil.rmtree("/root/.multichain/" + str(chain_name))
    call("multichaind", str(chain_name) + "@" + str(ip) + ":" + str(port), "-daemon", "-autosubscribe=streams")
    call("ipfs", "daemon")
    time.sleep(2)
    json_myaddr = apirpc.getaddresses
    json_addr = apirpc.liststreamkeyitems("default_account", "address")
    json_priv = apirpc.liststreamkeyitems("default_account", "privkey")

    hex_addr = json_addr[0]['data']
    hex_priv = json_priv[0]['data']
    my_addr = json_myaddr[0]

    default_privkey = hex_priv.decode("hex")
    default_address = hex_addr.decode("hex")

    apirpc.importaddress(default_address)
    txid = apirpc.createrawsendfrom(default_address, '{"my_addr":0}')
    signed_hex_json = apirpc.signrawtransaction(txid, "null", "[" + str(default_privkey) + "]")
    signed_hex = signed_hex_json['hex']
    apirpc.sendrawtransaction(signed_hex)

    print("Please wait...")
    time.sleep(20)

    hex_nick = nickname.encode("hex")
    apirpc.publish("nickname_resolve", "pseudo", str(hex_nick))

    print("---------- Finished ------------")

    set_chain_name(chain_name)


def create_chain(chain_name, nickname):
    """ Create a new chain where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    set_chain_name(chain_name)
    call("multichain-cli " + chain_name + " stop", shell=True)
    time.sleep(2)
    #call("firewall-cmd", "--permanent", "--zone=public", "--add-port=" + port + "/tcp")
    #call("systemctl", "restart", "firewalld.service")
    call('rm -rf /root/.multichain/' + chain_name, shell=True)
    call("multichain-util create " + chain_name + " -default-network-port=" + default_chain_port + " -default-rpc-port=" + default_rpc_port + " -anyone-can-connect=true -anyone-can-create=true -anyone-can-mine=true -anyone-can-receive=true", shell=True)
    call("multichaind " + chain_name + " -daemon -autosubscribe=streams", shell=True)

    time.sleep(5)

    apirpc = get_api()

    json_rep = apirpc.createkeypairs()
    address = json_rep[0]['address']
    pubkey = json_rep[0]['pubkey']
    privkey = json_rep[0]['privkey']

    print(apirpc.create("stream", "default_account", False))
    print(apirpc.send(address, 0))

    hex_addr = address.encode("hex")
    hex_priv = privkey.encode("hex")

    time.sleep(2)

    print(apirpc.publish("default_account", "address", hex_addr))
    print(apirpc.publish("default_account", "pubkey", pubkey))
    print(apirpc.publish("default_account", "privkey", hex_priv))

    print(apirpc.create("stream", "nickname_resolve", True))

    time.sleep(2)

    hex_nick = nickname.encode("hex")

    #a modifier avec les groupes : 
    print(apirpc.publish("nickname_resolve", "nickname", hex_nick))
    #apirpc.publish("nickname_resolve", "pubkey", pubkey)
    print('create chain finished')

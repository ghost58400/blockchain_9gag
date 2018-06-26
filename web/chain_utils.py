import binascii
import os
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


def get_state():
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/state.txt', 'r')
    val = file.read()
    file.close()
    val = val.replace('\n', '')
    return val


def set_state(state):
    file = open(os.path.dirname(os.path.realpath(__file__)) + '/state.txt', 'w')
    file.write(state)
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
    """ Returns the most recent nickname associated with the address passed by argument. """
    nicknames = api.liststreamitems('nickname_resolve')
    ret = None
    for nickname in nicknames:
        if nickname['publishers'][0] == account:
            ret = binascii.unhexlify(nickname['data'])
    return ret

def resolve_address(pubkey, api):
    """ Return the address of user 'nickname', None if user not found.
    Warning : function does not handle th situation where different users have the same nickname"""
    nicknames = api.liststreamitems('nickname_resolve')
    for nickname in nicknames:
        if nickname['key'] == pubkey:
            return nick['publishers'][0]
    return None

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

def connect_chain(ip="172.17.0.2", port="1234", chain_name="chain1", nickname="user"):
    """ Connect to the chain at 'ip' address where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    set_chain_name(chain_name)
    set_state('Connecting to chain ' + get_chain_name())

    call("multichain-cli " + chain_name + " stop", shell=True)
    time.sleep(2)
    call('rm -rf /root/.multichain/' + chain_name, shell=True)

    call("multichaind " + chain_name + "@" + ip + ":" + port + " -daemon -autosubscribe=streams", shell=True)
    time.sleep(2)

    apirpc = get_api()
    json_myaddr = apirpc.getaddresses()
    json_addr = apirpc.liststreamkeyitems("default_account", "address")
    json_priv = apirpc.liststreamkeyitems("default_account", "privkey")

    hex_addr = json_addr[0]['data']
    hex_priv = json_priv[0]['data']
    my_addr = json_myaddr[0]

    default_privkey = hex_priv.decode("hex")
    default_address = hex_addr.decode("hex")

    print(apirpc.importaddress(default_address))

    txid = apirpc.createrawsendfrom(default_address, {my_addr:0})
    signed_hex_json = apirpc.signrawtransaction(txid, None, [default_privkey])

    signed_hex = signed_hex_json['hex']
    print(apirpc.sendrawtransaction(signed_hex))

    print("Please wait...")
    time.sleep(20)

    # a revoir
    pubkey = apirpc.getaddresses(True)[0]['pubkey']
    print(pubkey)
    hex_nick = nickname.encode("hex")
    apirpc.publish("nickname_resolve", pubkey, str(hex_nick))

def create_chain(chain_name="chain1", nickname="admin"):
    """ Create a new chain where 'chain_name' is the name of the chain you want to create and where 'nickname' is the nickname you want to be identified by."""
    set_chain_name(chain_name)
    set_state('Creating chain ' + get_chain_name())
    call("multichain-cli " + chain_name + " stop", shell=True)
    time.sleep(2)
    # call("firewall-cmd", "--permanent", "--zone=public", "--add-port=" + port + "/tcp")
    # call("systemctl", "restart", "firewalld.service")
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

    # a modifier avec les groupes :
    print(apirpc.publish("nickname_resolve", pubkey, str(hex_nick)))
    # apirpc.publish("nickname_resolve", "pubkey", pubkey)
    print('create chain finished')

def create_group(chain_name, group_name, pubkey):
    """ Create a group in chain 'chain_name', with the name 'group_name' and composed with
    the user identified by the pubkey 'pubkey'.
    Ex usage: createGroup("chain1", "insa_group", "09ab5...") """
    apirpc = get_api()
    streamname = binascii.hexlify("[Group]" + str(group_name))
    apirpc.create('stream', streamname, False)
    apirpc.publish(streamname, pubkey, '')

def add_to_group(chain_name, group_name, pubkey):
    """ Add the user identified by 'pubkey' to to the group 'group_name' in 'chain_name' """
    apirpc = get_api()
    streamname = binascii.hexlify("[Group]" + str(group_name))
    apirpc.publish(streamname, pubkey, '')
    address = resolve_address(pubkey, apirpc)
    if address is None:
        print("Couldn't grant permission to add other people to the group.")
    else:
        apirpc.grant(address, streamname + ".write")


def post_group(chain_name, group_name, name_post, file, type):
    """ Post a file in a group """
    apirpc = get_api()
    api = ipfsapi.connect('127.0.0.1', 5001)
    res = api.add(file)
    streamname = binascii.hexlify("[" + str(group_name) + "]" + str(name_post))
    groupstream = binascii.hexlify("[Group]" + str(group_name))
    apirpc.create('stream', streamname, False)
    listkeys = apirpc.liststreamkeys(groupstream)

    value = json.dumps({'ipfs': binascii.hexlify(res['Hash']), 'type': binascii.hexlify(str(type))})
    for key in listkeys:
        # à finir
        apirpc.publish(streamname, 'ipfs', binascii.hexlify(res['Hash']))
        apirpc.publish(streamname, 'type', binascii.hexlify(sys.argv[4]))

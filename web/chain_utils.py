import binascii
import os
import time
from subprocess import call
from Savoir import Savoir
from consts import *
import ipfsapi
import rsa
import json
from Naked.toolshed.shell import muterun_js
import psutil


def kill_old_daemon():
    for proc in psutil.process_iter():
        if proc.name() == 'multichaind':
            call('kill ' + str(proc.pid), shell=True)
            time.sleep(2)



ethaddr = ''

def get_myaddr():
    api = get_api()
    listaddr = api.getaddresses(True)
    for addr in listaddr:
        if addr['ismine']:
            return addr['address']
    return None

def createEtherAddr():
    response = muterun_js('/root/scriptTest/createAccount.js')
    if response.exitcode == 0:
      addr = response.stdout[:-1]
      ethaddr = addr
    else:
      print('create Ethereum address error')

def get_ethaddr():
    return ethaddr


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

def generate_key_pair():
    """ Generate two files in the keys/ folder, with your public and private rsa key """
    (pubkey, privkey) = rsa.newkeys(2048)
    with open("/root/keys/public.pem", "w") as f:
        f.write(pubkey.save_pkcs1())
    with open("/root/keys/private.pem", "w") as f:
        f.write(privkey.save_pkcs1())

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

    try:
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
    except:
        print("Cannot get API")
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
    """ Return the address of user identified by 'pubkey'"""
    nicknames = api.liststreamitems('nickname_resolve')
    for nickname in nicknames:
        if nickname['key'] == pubkey:
            return nickname['publishers'][0]
    return None

def resolve_group(group_tag, api):
    """ Return the full name of a group from its tag """
    streamname = "[Group]" + binascii.hexlify(str(group_tag))
    listitems = api.liststreamitems(streamname)
    for key in listitems:
        if key['key'] == 'name':
            return binascii.unhexlify(key['data'])
    return "Group not found"

def get_all_posts(api, from_group=''):
    """ If you want to get only the posts from a specific group, set the optional parameter 'from_group' to the group tag you want to filter """
    print('in get all posts')
    print(api)
    if api is None:
        return []
    fsapi = ipfsapi.connect('127.0.0.1', 5001)
    raw_stream_names = api.liststreams()
    streams = []
    with open('/root/keys/public.pem', mode='rb') as f:
        pubkey = f.read()
    with open('/root/keys/private.pem', mode='rb') as f:
        private = f.read()
    private = rsa.PrivateKey.load_pkcs1(private)

    for stream in raw_stream_names:
        if stream['name'] != 'root' and stream['name'] != 'default_account' and stream['name'] != 'nickname_resolve':
            streams.append(stream['name'])

    posts = []
    for stream_name in streams:
        nameFound = False
        contentFound = False
        if stream_name[0] != '[' and from_group == '':
            stream = api.liststreamitems(stream_name)
            ipfs = ''
            type_contenu = ''
            author_account = ''
            sm_address = ''
            for it in stream:
                nom = binascii.unhexlify(it['title'])
                if it['key'] == 'ipfs':
                    ipfs = binascii.unhexlify(it['data'])
                    author_account = it['publishers'][0]
                if it['key'] == 'type':
                    type_contenu = binascii.unhexlify(it['data'])
                if it['key'] == 'smartcontract':
                    sm_address = binascii.unhexlify(it['data'])
            if ipfs != '' and type_contenu != '' and author_account != '':
                author = resolve_name(author_account, api)
                posts.append({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author, 'smartcontract': sm_address})
        elif stream_name[0:7] != "[Group]":
            group_tag = stream_name[1:4]
            if from_group != '' and from_group != group_tag:
                continue
            stream = api.liststreamitems(stream_name)
            myaddr = get_myaddr()
            for it in stream:
                if it['key'] == 'title':
                    nom = binascii.unhexlify(it['data'])
                    nameFound = True
                elif it['key'] == myaddr:
                    content = rsa.decrypt(binascii.unhexlify(it['data']), private).decode('utf8')
                    content = json.loads(content)
                    ipfs = binascii.unhexlify(content['ipfs'])
                    author_account = it['publishers'][0]
                    type_contenu = binascii.unhexlify(content['type'])
                    author = resolve_name(author_account, api)
                    contentFound = True
            if contentFound and nameFound:
                posts.append({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author})
                print(json.dumps({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author}))

    for post in posts:
        if post['type'] == 'Image':
            post['ipfs'] = 'https://ipfs.io/ipfs/' + post['ipfs']
        else:
            post['ipfs'] = fsapi.get_json(post['ipfs'])
    return posts


def connect_chain(ip, port, chain_name, nickname):
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
    generate_key_pair()
    apirpc.publish("nickname_resolve", pubkey, str(hex_nick))
    set_state('Connected to ' + chain_name)


def create_chain(chain_name, nickname):
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
    print('api :')
    print(apirpc)

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
    generate_key_pair()
    # a modifier avec les groupes :
    print(apirpc.publish("nickname_resolve", pubkey, str(hex_nick)))
    # apirpc.publish("nickname_resolve", "pubkey", pubkey)
    print('create chain finished')
    set_state('Connected to ' + chain_name)


def deployContractForPost():
    response = muterun_js('/root/scriptTest/EtherUtils.js')
    if response.exitcode == 0:
      addr = response.stdout[:-1]
      return addr
    else:
      print('Deploy contract error')
      return ''


def create_post(title, content, type):
    apirpc = get_api()
    if apirpc is None:
        return 'not connected'
    api = ipfsapi.connect('127.0.0.1', 5001)
    streamname = binascii.hexlify(title)[0:32]
    if type == 'Text':
        res = api.add_json(content)
    if type == 'Image':
        res = api.add(content)
        res = res['Hash']

    print(res)

    apirpc.create('stream', streamname, False)
    apirpc.publish(streamname, 'title', binascii.hexlify(title))
    apirpc.publish(streamname, 'ipfs', binascii.hexlify(res))
    apirpc.publish(streamname, 'type', binascii.hexlify(type))
    # Decommenter apres lancer la VM Ethereum et executer scriptTest/test2.sh
    #addr = deployContractForPost()
    #apirpc.publish(streamname, 'smartcontract', binascii.hexlify(addr))
    print(apirpc.liststreamitems(streamname))
    return 'ok'


def create_group(chain_name="chain1", group_tag="PGM", group_name="Pro Gamers"):
    """ Create a group in chain 'chain_name', with the name 'group_tag'.
    Ex usage: createGroup("chain1", "insa_group") """
    apirpc = get_api()
    with open('/root/keys/public.pem', mode='rb') as f:
        pubkey = f.read()
    streamname = ("[Group]" + binascii.hexlify(str(group_tag)))[0:32]
    apirpc.create('stream', streamname, False)
    apirpc.publish(streamname, 'name', binascii.hexlify(group_name))
    apirpc.publish(streamname, get_myaddr(), binascii.hexlify(pubkey))

def join_group(chain_name="chain1", group_tag="PGM"):
    """ Join a group in chain 'chain_name', with the name 'group_tag'.
    Ex usage: createGroup("chain1", "insa_group") """
    apirpc = get_api()
    with open('/root/keys/public.pem', mode='rb') as f:
        pubkey = f.read()
    streamname = ("[Group]" + binascii.hexlify(str(group_tag)))[0:32]
    apirpc.publish(streamname, get_myaddr(), binascii.hexlify(pubkey))

def add_to_group(address, chain_name="chain1", group_tag="PGM"):
    """ Add the user identified by 'address' to the group 'group_tag' in 'chain_name' """
    apirpc = get_api()
    streamname = ("[Group]" + binascii.hexlify(str(group_tag)))[0:32]
    apirpc.grant(address, streamname + ".write")

def post_group(name_post, file, type, chain_name="chain1", group_tag="PGM"):
    """ Post a file in a group """
    apirpc = get_api()
    api = ipfsapi.connect('127.0.0.1', 5001)
    res = api.add(file)
    streamname = ("[" + str(group_tag) + "]" + binascii.hexlify(str(name_post)))[0:31]
    groupstream = ("[Group]" + binascii.hexlify(str(group_tag)))[0:32]
    apirpc.create('stream', streamname, False)
    listkeys = apirpc.liststreamitems(groupstream)


    message = json.dumps({'ipfs': binascii.hexlify(res['Hash']), 'type': binascii.hexlify(str(type))}).encode('utf8')
    apirpc.publish(streamname, 'title', binascii.hexlify("[" + str(group_tag) + "]" + str(name_post)))

    for key in listkeys:
        if key['key'] == 'name':
            continue
        print(binascii.unhexlify(key['data']))
        print(key['key'])
        pubkey = rsa.PublicKey.load_pkcs1(binascii.unhexlify(key['data']))
        crypto = rsa.encrypt(message, pubkey)
        apirpc.publish(streamname, key['key'], binascii.hexlify(crypto))


# WORK IN PROGRESS
# def get_all_posts_group(api, group_name="illuminati"):
#     """ EXTREME """
#     posts = []
#     groupstream = ("[Group]" + binascii.hexlify(str(group_name)))[0:32]
#     with open('/root/keys/public.pem', mode='rb') as f:
#         pubkey = f.read()
#     with open('/root/keys/private.pem', mode='rb') as f:
#         private = f.read()
#     private = rsa.PrivateKey.load_pkcs1(private)
#     raw_stream_names = api.liststreams()
#     streams = []
#     for stream in raw_stream_names:
#         if stream['name'] != 'root' and stream['name'] != 'default_account' and stream['name'] != 'nickname_resolve' and stream['name'][0] == '[' and stream['name'][0:7] != "[Group]":
#             streams.append(stream['name'])
#     for content in streams:
#         liststream = api.liststreamkeyitems(content, binascii.hexlify(pubkey))
#         print(liststream)
#         nom = '[' + binascii.unhexlify(liststream[1:])
#         if nom.find("[" + str(group_name) + "]") < 0:
#             continue
#         content = binascii.unhexlify(rsa.decrypt(content['data'], private)).decode('utf8')
#         content = json.load(content)
#         ipfs = content['ipfs']
#         author_account = content['publishers'][0]
#         type_contenu = content['type']
#         author = resolve_name(author_account, api)
#         posts.append({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author})
#         print(json.dumps({'title': nom, 'ipfs': ipfs, 'type': type_contenu, 'author': author}))
#     return posts

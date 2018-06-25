import binascii

from Savoir import Savoir

default_rpc_port = '1235'
default_rpc_host = '127.0.0.1'


def get_chain_name():
    file = open('chain_name.txt', 'r')
    val = file.read()
    file.close()
    return val


def set_chain_name(name):
    file = open('chain_name.txt', 'w')
    file.write(name)
    file.close()


def get_api(host=default_rpc_host, port=default_rpc_port, chain_name=get_chain_name()):
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


def connect_chain(ip, port, chain_name):
    # heavy stuff
    set_chain_name(chain_name)


def create_chain(chain_name):
    # heavy stuff
    set_chain_name(chain_name)

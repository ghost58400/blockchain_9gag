import binascii
from Savoir import Savoir


def get_api(host, port, chain_name):
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
    #ajouter prise en compte du plus recent, pour changement pseudo
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
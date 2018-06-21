import sys,os
import binascii

from Savoir import Savoir
import ipfsapi
#except:
 # print("You need to install ipfs and/or Savoir, see googledocs instructions")
  #sys.exit(-1)


rpcuser = 'multichainrpc'
rpcpasswd = '5guEVbZK2QuES9o8o5GuCiDCkitMAaL9twFmC78now7U'
rpchost = '127.0.0.1'
rpcport = '1235'
chainname = 'chain1'

apirpc = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
# on se connecte au noeud IPFS
api = ipfsapi.connect('127.0.0.1', 5001)

#on ajoute le fichier
s = apirpc.liststreams()
streams = []
for i in s:
  if i['name'] != 'root' and i['name'] != 'default_account': 
    streams.append(i['name'])

posts = []
for item in streams:
  stream = apirpc.liststreamitems(item)
  for it in stream:
    if it['key'] == 'name':
      nom = binascii.unhexlify(it['data'])
    if it['key'] == 'ipfs':
      ipfs = binascii.unhexlify(it['data'])
  posts.append({'name': nom,'ipfs': ipfs })

print(posts)
for item in posts:
  print(item['name'])
  print(api.cat(item['ipfs']))

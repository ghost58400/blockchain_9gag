import sys,os
from Naked.toolshed.shell import muterun_js
from Savoir import Savoir
import ipfsapi
import binascii
#except:
 # print("You need to install ipfs and/or Savoir, see googledocs instructions")
  #sys.exit(-1)

#create stream  <nom du stream> false
#listpermissions <nom du stream>.*

#on teste le fichier a poster
if len(sys.argv) < 5:
  print("Usage: <file> <name post> <chain> <type>")
  sys.exit(-1)

chainname = str(sys.argv[3])
pathconf = "/root/.multichain/" + chainname + "/multichain.conf"
rpcuser = ""
rpcpassword = ""

with open(pathconf,"r") as f:
    line_list = [c for c in f.readlines()]
    for line in line_list:
        if "rpcuser=" in line:
            rpcuser = line.split("=")[1]
        elif "rpcpassword=" in line:
            rpcpassword = line.split("=")[1]
    if rpcuser == "":
        print("Couldn't retrieve rpcuser from " + chainname)
        sys.exit(-1)
    elif rpcpassword == "":
        print("Couldn't retrieve rpcpassword from " + chainname)
        sys.exit(-1)

rpcuser = rpcuser.replace('\n', '')
rpcpassword = rpcpassword.replace('\n', '')

rpchost = '127.0.0.1'
rpcport = '1235'

apirpc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
# on se connecte au noeud IPFS
api = ipfsapi.connect('127.0.0.1', 5001)


#on ajoute le fichier
res = api.add(sys.argv[1])
print(res)
response = muterun_js('/root/scriptTest/deploy.js')
if response.exitcode == 0:
  addr = response.stdout[:-1]
  print(addr)
else:
  print('Deploy contract error')
  sys.exit(-1)
streamname = binascii.hexlify(sys.argv[2])

apirpc.create('stream', streamname, False)
apirpc.publish(streamname, 'ipfs', binascii.hexlify(res['Hash']))
apirpc.publish(streamname, 'type', binascii.hexlify(sys.argv[4]))
apirpc.publish(streamname, 'smartcontract', binascii.hexlify(addr))
print(apirpc.liststreamitems(sys.argv[3]))

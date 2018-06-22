import sys,os

from Savoir import Savoir
import ipfsapi
#except:
 # print("You need to install ipfs and/or Savoir, see googledocs instructions")
  #sys.exit(-1)

#create stream  <nom du stream> false
#listpermissions <nom du stream>.*

#on teste le fichier a poster
if len(sys.argv) < 5:
  print("Usage: <file> <name post> <stream> <chain>")
  sys.exit(-1)

chainname = str(sys.argv[4])
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

rpchost = '127.0.0.1'
rpcport = '1235'

apirpc = Savoir(rpcuser, rpcpassword, rpchost, rpcport, chainname)
# on se connecte au noeud IPFS
api = ipfsapi.connect('127.0.0.1', 5001)

ext_allowed = ["png", "jpg", "jpeg", "txt", "bmp", "gif"]

ext = os.path.splitext(sys.argv[1])[1][1:]

if ext not in ext_allowed:
  print("Extension not allowed...")
  print(ext_allowed)
  sys.exit(-1)

#on ajoute le fichier
res = api.add(sys.argv[1])
print(res)
apirpc.create('stream', sys.argv[3], False)
apirpc.publish(sys.argv[3], "ipfs", binascii.hexlify(res['Hash']))
apirpc.publish(sys.argv[3], "name", binascii.hexlify(sys.argv[2]))
print(apirpc.liststreamitems(sys.argv[3]))

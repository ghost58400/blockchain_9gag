from Savoir import Savoir
import ipfsapi
#except:
 # print("You need to install ipfs and/or Savoir, see googledocs instructions")
  #sys.exit(-1)

#create stream  <nom du stream> false
#listpermissions <nom du stream>.*

#on teste le fichier a poster
if len(sys.argv) < 4:
  print("Usage: <file> <name post> <stream>")
  sys.exit(-1)

rpcuser = 'multichainrpc'
rpcpasswd = '5guEVbZK2QuES9o8o5GuCiDCkitMAaL9twFmC78now7U'
rpchost = '127.0.0.1'
rpcport = '1235'
chainname = 'chain1'

apirpc = Savoir(rpcuser, rpcpasswd, rpchost, rpcport, chainname)
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


import sys,os

try:
  import ipfsapi
except:
  print("You need to install ipfs, see googledocs instructions")
  sys.exit(-1)

#create stream  <nom du stream> false
#listpermissions <nom du stream>.*

#on teste le fichier à poster
if len(sys.argv) < 2:
  print("Need a file to post bro...")
  sys.exit(-1)

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
#print(api.cat(res['Hash']))

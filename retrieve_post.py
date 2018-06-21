import sys

try:
  import ipfsapi
except:
  print("Install ipfs...")
  sys.exit(-1)

if len(sys.argv) < 2:
  print("Input an hash to retrieve the file")
  sys.exit(-1)

hash = sys.argv[1]

#liststreams
#liststreamitems <nom du stream> <key>

api = ipfsapi.connect('127.0.0.1', 5001)
print(api.cat(hash))

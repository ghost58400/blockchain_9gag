#!/usr/bin/env bash

chain_name=chain1
ip=192.168.32.146
port=1234

multichain-cli $chain_name stop
sleep 2
rm -rf ~/.multichain/$chain_name

multichaind $chain_name@$ip:$port -daemon -autosubscribe=streams
sleep 2

json_myaddr=$(multichain-cli $chain_name getaddresses)
json_addr=$(multichain-cli $chain_name liststreamkeyitems default_account address)
json_priv=$(multichain-cli $chain_name liststreamkeyitems default_account privkey)

hex_addr=$(echo $json_addr | python -c "import sys, json; print json.load(sys.stdin)[0]['data']")
hex_priv=$(echo $json_priv | python -c "import sys, json; print json.load(sys.stdin)[0]['data']")
my_addr=$(echo $json_myaddr | python -c "import sys, json; print json.load(sys.stdin)[0]")

default_privkey=$(echo $hex_priv | xxd -p -r)
default_address=$(echo $hex_addr | xxd -p -r)

#multichain-cli $chain_name importprivkey $default_privkey
#multichain-cli $chain_name sendfrom $default_address $my_addr 0

multichain-cli $chain_name importaddress $default_address
txid=$(multichain-cli $chain_name createrawsendfrom $default_address {\"$my_addr\":0})
signed_hex_json=$(multichain-cli $chain_name signrawtransaction $txid null \[\"$default_privkey\"])
signed_hex=$(echo $signed_hex_json | python -c "import sys, json; print json.load(sys.stdin)['hex']")
multichain-cli $chain_name sendrawtransaction $signed_hex

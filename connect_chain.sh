#!/usr/bin/env bash

if [ $# -ne 2 ]
  then
    echo "Usage : connect_chain.sh IP NICKNAME"
    echo "Where IP is the ip address of the node you want to connect to and where NICKNAME is the nickname you want to be identified by."
    exit
fi

chain_name=chain1
ip=$1
nickname=$2
port=1234

multichain-cli $chain_name stop
sleep 2
rm -rf ~/.multichain/$chain_name

multichaind $chain_name@$ip:$port -daemon -autosubscribe=streams
ipfs daemon &
sleep 2

json_myaddr=$(multichain-cli $chain_name getaddresses)
json_addr=$(multichain-cli $chain_name liststreamkeyitems default_account address)
json_priv=$(multichain-cli $chain_name liststreamkeyitems default_account privkey)

hex_addr=$(echo -n $json_addr | python -c "import sys, json; print json.load(sys.stdin)[0]['data']")
hex_priv=$(echo -n $json_priv | python -c "import sys, json; print json.load(sys.stdin)[0]['data']")
my_addr=$(echo -n $json_myaddr | python -c "import sys, json; print json.load(sys.stdin)[0]")

default_privkey=$(echo -n $hex_priv | xxd -p -r)
default_address=$(echo -n $hex_addr | xxd -p -r)

#multichain-cli $chain_name importprivkey $default_privkey
#multichain-cli $chain_name sendfrom $default_address $my_addr 0

multichain-cli $chain_name importaddress $default_address
txid=$(multichain-cli $chain_name createrawsendfrom $default_address {\"$my_addr\":0})
signed_hex_json=$(multichain-cli $chain_name signrawtransaction $txid null \[\"$default_privkey\"])
signed_hex=$(echo -n $signed_hex_json | python -c "import sys, json; print json.load(sys.stdin)['hex']")
multichain-cli $chain_name sendrawtransaction $signed_hex

sleep 20

hex_nick=$(echo -n $nickname | xxd -p -c 99999)
multichain-cli $chain_name publish nickname_resolve pseudo $hex_nick

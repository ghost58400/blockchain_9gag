#!/usr/bin/env bash

if [ $# -ne 2 ]
  then
    echo "Usage : create_chain.sh CHAIN_NAME NICKNAME"
    echo "Where CHAIN_NAME is the name of the chain you want to create and where NICKNAME is the nickname you want to be identified by."
    exit
fi


chain_name=$1
port=1234
nickname=$2
rpc_port=1235

multichain-cli $chain_name stop
sleep 2
firewall-cmd --permanent --zone=public --add-port=$port/tcp
systemctl restart firewalld.service
rm -rf ~/.multichain/$chain_name

multichain-util create $chain_name -default-network-port=$port -default-rpc-port=$rpc_port -anyone-can-connect=true -anyone-can-create=true -anyone-can-mine=true -anyone-can-receive=true

multichaind $chain_name -daemon -autosubscribe=streams
ipfs daemon &

json=$(multichain-cli $chain_name createkeypairs)
address=$(echo -n $json | python -c "import sys, json; print json.load(sys.stdin)[0]['address']")
pubkey=$(echo -n $json | python -c "import sys, json; print json.load(sys.stdin)[0]['pubkey']")
privkey=$(echo -n $json | python -c "import sys, json; print json.load(sys.stdin)[0]['privkey']")

multichain-cli $chain_name create stream default_account false

multichain-cli $chain_name send $address 0

hex_addr=$(echo -n $address | xxd -p -c 99999)
hex_priv=$(echo -n $privkey | xxd -p -c 99999)

multichain-cli $chain_name publish default_account address $hex_addr
multichain-cli $chain_name publish default_account pubkey $pubkey
multichain-cli $chain_name publish default_account privkey $hex_priv

multichain-cli $chain_name create stream nickname_resolve true

hex_nick=$(echo -n $nickname | xxd -p -c 99999)
multichain-cli $chain_name publish nickname_resolve pseudo $hex_nick

ipfs daemon &

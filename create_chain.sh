#!/usr/bin/env bash

chain_name=chain1
port=1234

multichain-cli $chain_name stop
sleep 2
firewall-cmd --permanent --zone=public --add-port=$port/tcp
systemctl restart firewalld.service
rm -rf ~/.multichain/$chain_name

multichain-util create $chain_name -default-network-port=$port -anyone-can-connect=true -anyone-can-create=true -anyone-can-mine=true -anyone-can-receive=true

multichaind $chain_name -daemon -autosubscribe=streams

json=$(multichain-cli $chain_name createkeypairs)
address=$(echo $json | python -c "import sys, json; print json.load(sys.stdin)[0]['address']")
pubkey=$(echo $json | python -c "import sys, json; print json.load(sys.stdin)[0]['pubkey']")
privkey=$(echo $json | python -c "import sys, json; print json.load(sys.stdin)[0]['privkey']")

multichain-cli $chain_name create stream default_account false

multichain-cli $chain_name send $address 0

hex_addr=$(echo $address | xxd -p -c 99999)
hex_priv=$(echo $privkey | xxd -p -c 99999)

multichain-cli $chain_name publish default_account address $hex_addr
multichain-cli $chain_name publish default_account pubkey $pubkey
multichain-cli $chain_name publish default_account privkey $hex_priv

ipfs daemon &

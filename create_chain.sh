#!/usr/bin/env bash

chain_name=chain1
port=1234
nickname=admin

multichain-cli $chain_name stop
sleep 2
firewall-cmd --permanent --zone=public --add-port=$port/tcp
systemctl restart firewalld.service
rm -rf ~/.multichain/$chain_name

multichain-util create $chain_name -default-network-port=$port -anyone-can-connect=true -anyone-can-create=true -anyone-can-mine=true -anyone-can-receive=true

multichaind $chain_name -daemon -autosubscribe=streams

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

sleep 10

hex_nick=$(echo -n $nickname | xxd -p -c 99999)
multichain-cli $chain_name publish nickname_resolve pseudo $hex_nick

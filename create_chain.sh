#!/bin/bash

chain_name=chain1
port=1234

multichain-util create $chain_name -default-network-port=$port
sed -i -e "s/anyone-can-connect = false/anyone-can-connect = true /g" ~/.multichain/$chain_name/params.dat
sed -i -e "s/anyone-can-create = false/anyone-can-create = true /g" ~/.multichain/$chain_name/params.dat
sed -i -e "s/anyone-can-mine = false/anyone-can-mine = true /g" ~/.multichain/$chain_name/params.dat
multichaind $chain_name -daemon

firewall-cmd --permanent --zone=public --add-port=$port/tcp
systemctl restart firewalld.service

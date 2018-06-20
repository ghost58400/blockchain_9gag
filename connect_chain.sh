#!/bin/bash

chain_name=chain1
ip=192.168.43.117
port=1234

multichaind $chain_name@$ip:$port -daemon

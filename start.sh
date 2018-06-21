#!/usr/bin/env bash

chain_name=chain1

multichaind $chain_name -daemon
ipfs daemon

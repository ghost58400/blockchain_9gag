#!/usr/bin/env bash

chain_name=chain1

dhclient
multichaind $chain_name -daemon

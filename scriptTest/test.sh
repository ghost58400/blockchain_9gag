#!/usr/bin/env bash

ip=$1
sed -i -e "s/localhost:8545*/$ip/g" index.js
sed -i -e "s/localhost:8545*/$ip/g" EtherUtils.js
sed -i -e "s/localhost:8545*/$ip/g" createAccount.js
sed -i -e "s/localhost:8545*/$ip/g" /root/web/static/post/post.js
sed -i -e "s/localhost:8545*/$ip/g" /root/web/static/group/group.js

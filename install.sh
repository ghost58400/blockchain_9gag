#!/usr/bin/env bash

dhclient
echo dhclient >> /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local
yum -y --enablerepo=extras install epel-release
yum update -y
yum install -y nano wget ntpdate vim-common python-pip
pip install --upgrade pip
pip install flask
pip install Savoir
pip install ipfsapi
#remplacer from Savoir.Savoir import *
#par from Savoir import Savoir
#dans /usr/lib/python2.7/site-packages/Savoir/__init__.py
sed -i -e "s/from Savoir.Savoir import */from Savoir import Savoir/g" /usr/lib/python2.7/site-packages/Savoir/__init__.py

ntpdate pool.ntp.org

rm -rf ~/.multichain
cd /tmp
wget https://dist.ipfs.io/ipfs-update/v1.5.2/ipfs-update_v1.5.2_linux-amd64.tar.gz
tar -xvzf ipfs-update_v1.5.2_linux-amd64.tar.gz
cd ipfs-update
sh install.sh
cd ..
ipfs-update install latest
ipfs init
wget https://www.multichain.com/download/multichain-1.0.5.tar.gz
tar -xvzf multichain-1.0.5.tar.gz
cd multichain-1.0.5
mv multichaind multichain-cli multichain-util /usr/bin/
ip a

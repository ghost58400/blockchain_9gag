#!/usr/bin/env bash

dhclient
echo dhclient >> /etc/rc.d/rc.local
chmod +x /etc/rc.d/rc.local
echo ip a >> ~/.bashrc
yum update -y
yum install -y nano wget ntpdate vim-common
ntpdate pool.ntp.org

rm -rf ~/.multichain
cd /tmp
wget https://www.multichain.com/download/multichain-1.0.5.tar.gz
tar -xvzf multichain-1.0.5.tar.gz
cd multichain-1.0.5
mv multichaind multichain-cli multichain-util /usr/bin/
ip a

#!/bin/bash

dhclient
yum update -y
yum install -y nano wget htop ntpdate
ntpdate pool.ntp.org

cd /tmp
wget https://www.multichain.com/download/multichain-1.0.5.tar.gz
tar -xvzf multichain-1.0.5.tar.gz
cd multichain-1.0.5
mv multichaind multichain-cli multichain-util /usr/bin/


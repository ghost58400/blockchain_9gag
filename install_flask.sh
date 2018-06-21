#!/bin/sh

yum --enablerepo=extras install epel-release
yum -y install python 
yum -y install python-pip

pip install flask
pip install -U flask-cors


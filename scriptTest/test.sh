echo "Enter <ip>:<port> of Etherum-VM"
read ip
sed -i -e "s/localhost:8545*/$ip/g" index.js
sed -i -e "s/localhost:8545*/$ip/g" EtherUtils.js
sed -i -e "s/localhost:8545*/$ip/g" createAccount.js
sed -i -e "s/localhost:8545*/$ip/g" /root/web/static/post/post.js

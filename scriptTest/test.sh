npm install
npm install webpack
npm install solc
npm install web3
echo "Enter <ip>:<port> of Etherum-VM"
read ip
sed -i -e "s/localhost:8545*/$ip/g" index.js
sed -i -e "s/localhost:8545*/$ip/g" deploy.js
python html2.py
python -m SimpleHTTPServer 1337

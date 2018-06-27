provider = "http://localhost:8545"

//Create an account
function createAccount(){
  Web3 = require('web3');
  web3 = new Web3(new Web3.providers.HttpProvider(provider));
  addr = web3.eth.personal.newAccount('');
  web3.eth.getAccounts().then(e => {a = e[e.length-10];console.log(a)});
}

createAccount();

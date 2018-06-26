provider = "http://localhost:8545"

//Create an account
function createAccount(){
  Web3 = require('web3');
  web3 = new Web3(new Web3.providers.HttpProvider(provider));
  addr = web3.eth.personal.newAccount('');
  web3.eth.getAccounts().then(e => {a = e[e.length-1];web3.eth.personal.unlockAccount(a,'',500); deployContract(a);});
}

//Deploy a smart contract in the Ethereum BlockChain
function deployContract(addr) {

  //importing filesytem tools
  fs = require('fs');

  //importing web3js
  Web3 = require('web3');

  //Connection to Etherum VM node
  web3 = new Web3(new Web3.providers.HttpProvider(provider));
  
  //Getting the text of the smartcontract
  code = fs.readFileSync('/root/scriptTest/voting.sol').toString();

  //Importing Solidity compiler
  solc = require('solc');

  //Compiling...
  compiledCode = solc.compile(code);

  //Get abi Definition of the contract
  abiDefinition = JSON.parse(compiledCode.contracts[':Voting'].interface);

  //Creating contract at address
  VotingContract = new web3.eth.Contract(abiDefinition);

  //Getting byte code
  byteCode = compiledCode.contracts[':Voting'].bytecode;
  
  //Deploying contract
  return  deployedContract = VotingContract.deploy({data: byteCode}).send({from: addr, gas: 4700000}).then(function(contract){console.log(contract.options.address)});
}

function getAccount(nb) {
  Web3 = require('web3');
  web3 = new Web3(new Web3.providers.HttpProvider(provider));
  web3.eth.getAccounts().then(e => {addr=e[0];deployContract(addr)});
}

//createAccount();
getAccount(4);

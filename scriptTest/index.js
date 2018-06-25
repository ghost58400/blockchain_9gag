web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
VotingContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"upVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"Like","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"downVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesAgainst","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"Dislike","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);
// In your nodejs console, execute contractInstance.address to get the address at which the contract is deployed and change the line below to use your deployed address
contractInstance = VotingContract.at('0x4382e0dfb065c3566166ea9b8894a845cdb2f524');

function actualize() {
  let like = contractInstance.totalVotesFor.call().toString();
  let dis = contractInstance.totalVotesAgainst.call().toString();
  $("#like").html("Liked: "+like);
  $("#dislike").html(" | Disliked: "+dis);
}

function Like() {
  contractInstance.Like({from: web3.eth.accounts[0]});
  actualize();
}

function Dislike() {
  contractInstance.Dislike({from: web3.eth.accounts[0]});
  actualize();
}

$(document).ready(function() {
  actualize();
});

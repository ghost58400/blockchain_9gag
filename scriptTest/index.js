web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
VotingContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"upVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"Like","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"downVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesAgainst","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"Dislike","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);
// In your nodejs console, execute contractInstance.address to get the address at which the contract is deployed and change the line below to use your deployed address
nbPost = $('.container').length;

addrs = [];
$("img").each(function(i) {
  addr = $(this).attr('id');
  addrs.push(addr);
});

console.log(addrs);

contracts = [];
for(it = 0; it < addrs.length; it++){
  contractInstance = VotingContract.at(addrs[it]);
  contracts.push(contractInstance);
}

function actualize() {
  for(it = 0; it < contracts.length; it++){
    i = it + 1;
    let like = contracts[it].totalVotesFor.call().toString();
    let dis = contracts[it].totalVotesAgainst.call().toString();
    $("#like_"+i).text("Liked: "+like);
    $("#dislike_"+i).text(" | Disliked: "+dis);
  }
}


function Like(nb) {
  i = nb-1;
  contracts[i].Like({from: web3.eth.accounts[0]});
  let like = contracts[i].totalVotesFor.call().toString();
  let dis = contracts[i].totalVotesAgainst.call().toString();
  $("#like_"+nb).text("Liked: "+like);
  $("#dislike_"+nb).text(" | Disliked: "+dis);
}

function Dislike(nb) {
  i = nb-1;
  contracts[i].Dislike({from: web3.eth.accounts[0]});
  let like = contracts[i].totalVotesFor.call().toString();
  let dis = contracts[i].totalVotesAgainst.call().toString();
  $("#like_"+nb).text("Liked: "+like);
  $("#dislike_"+nb).text(" | Disliked: "+dis);

}

$(document).ready(function() {
  actualize();
});

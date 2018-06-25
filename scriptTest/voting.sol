pragma solidity ^0.4.11;

contract Voting {
  
  uint8 public upVotes;
  uint8 public downVotes;

  mapping(address => bool) alreadyUp;
  mapping(address => bool) alreadyDown;
  
  
  function Voting() {
    upVotes = 0;
    downVotes = 0;
  }

  function totalVotesFor() returns (uint8) {
    return upVotes;
  }

  function totalVotesAgainst() returns (uint8) {
    return downVotes;
  }

  function Like() {
    if(alreadyUp[msg.sender]){
        alreadyUp[msg.sender] = false;
        upVotes -= 1;
    }else{
        alreadyUp[msg.sender] = true;
        if(alreadyDown[msg.sender]){
          downVotes -= 1;
          alreadyDown[msg.sender] = false;
        }
        upVotes += 1;
    }
  }

  function Dislike() {
    if(alreadyDown[msg.sender]){
        alreadyDown[msg.sender] = false;
        downVotes -= 1;
    }else{
        alreadyDown[msg.sender] = true;
        if(alreadyUp[msg.sender]){
          upVotes -= 1;
          alreadyUp[msg.sender] = false;
        }
        downVotes +=1;
    }
    }

}


web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
VotingContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"upVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"Like","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"downVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesAgainst","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"Dislike","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);

angular.module('App.post', ['ngRoute', 'ngCookies'])

    .controller('PostController', function ($scope, $http, $cookies) {

        $scope.list_stream = null;
        $scope.current_post = null;

        $scope.new_post_title = null;
        $scope.new_post_content = null;
        $scope.new_post_type = 'Text';
        $scope.new_post_visibility = null;

        console.log("PostController");
        if(!$cookies.get("addrEth")){
            $http.get('/myetheraddr')
                .then(function success(e){
                  $cookies.put('addrEth', e.data);
                  //console.log($cookies.get("addrEth"))
                }, function error(e) {
                  console.log("error getting my Ethereum address");
                  $scope.errors = e.data.errors
                });
        }
        $http.get('/get_posts')
            .then(function success(e) {
                $scope.errors = [];
                if (e.data !== '')
                    console.log("/get_posts");
                    for(i=0; i < e.data.length; i++){
                      var sm_address = e.data[i].smartcontract;
                      console.log("listposts");
                      console.log(sm_address);
                      console.log("endlist_post");
                      var contract = VotingContract.at(sm_address);
                      e.data[i].upvotes = contract.totalVotesFor.call().toString();
                      e.data[i].downvotes = contract.totalVotesAgainst.call().toString();
                    }
                    $scope.list_stream = e.data;
                    console.log(e.data[0]);
            }, function error(e) {
                console.log("error get_posts");
                $scope.errors = e.data.errors;
            });


        $scope.upvote = function (stream) {
            var found = $scope.list_stream.find(function(element) {
                return element.title === stream.title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = stream.smartcontract;
                var addr = $cookies.get('addrEth');
                console.log(sm_address);
                var contract = VotingContract.at(sm_address);
                contract.Like({from: addr});
                $scope.stream = stream
                $scope.stream.upvotes = contract.totalVotesFor.call().toString();
                $scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
                console.log($scope.stream.upvotes);
            }

        };

        $scope.downvote = function (stream) {
            var found = $scope.list_stream.find(function(element) {
                return element.title === stream.title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = stream.smartcontract;
                var addr = $cookies.get('addrEth');
                console.log(sm_address);
                var contract = VotingContract.at(sm_address);
                contract.Dislike({from: addr});
                $scope.stream = stream
                $scope.stream.upvotes = contract.totalVotesFor.call().toString();
                $scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
                console.log($scope.stream.downvotes);
            }

        };
    });

//web3 = new Web3(new Web3.providers.HttpProvider("http://192.168.43.131:8545"));
//VotingContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"upVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"Like","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"downVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesAgainst","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"Dislike","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);

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
                  $cookies.put("addrEth", e.data);
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
                    $scope.list_stream = e.data;
                    console.log(e.data);
                    for(stream in $scope.list_stream){
                      var sm_address = stream.smartcontract;
                      var addr = $cookies.get('addrEth');
                      //var contract = VotingContract.at(sm_address);
                      //stream.upvotes = contract.totalVotesFor.call().toString();
                      //stream.downvotes = contract.totalVotesAgainst.call().toString();
                    }
                    console.log($scope.list_stream);
            }, function error(e) {
                console.log("error get_posts");
                $scope.errors = e.data.errors;
            });

        $scope.show_post = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
            }
        };

        $scope.upvote = function (addr, title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = addr;
                var addr = $cookies.get('addrEth');
                //var contract = VotingContract.at(sm_address);
                //contract.Like({from: addr});
                //$scope.stream = title
                //$scope.stream.upvotes = contract.totalVotesFor.call().toString();
                //$scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
            }
        };

        $scope.downvote = function (addr,title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = addr;
                var addr = $cookie.get('addrEth');
                //var contract = VotingContract.at(sm_address);
                //contract.Dislike({from: addr});
                //$scope.stream = title
                //$scope.stream.upvotes = contract.totalVotesFor.call().toString();
                //$scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
                
                
            }
        }
    });

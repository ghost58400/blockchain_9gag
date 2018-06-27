angular.module('App.post', ['ngRoute'])

    .controller('PostController', function ($scope, $http, $cookie) {

        $scope.list_stream = [];
        $scope.current_post = null;

        $scope.new_post_title = null;
        $scope.new_post_content = null;
        $scope.new_post_type = 'Text';
        $scope.new_post_visibility = null;

        console.log("PostController");

        $http.get('/get_posts')
            .then(function success(e) {
                $scope.errors = [];
                if (e.data !== '')
                    console.log("/get_posts");
                    $scope.list_stream = e.data;
                    for(stream in $scope.list_stream){
                      var sm_address = stream.smartcontract;
                      var addr = $cookie.get('addrEth');
                      var contract = VotingContract.at(sm_address);
                      stream.upvotes = contract.totalVotesFor.call().toString();
                      stream.downvotes = contract.totalVotesAgainst.call().toString();
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

        $scope.upvote = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = title.smartcontract;
                var addr = $cookie.get('addrEth');
                var contract = VotingContract.at(sm_address);
                contract.Like({from: addr});
                $scope.stream = title
                $scope.stream.upvotes = contract.totalVotesFor.call().toString();
                $scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
            }
        };

        $scope.downvote = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
                var sm_address = title.smartcontract;
                var addr = $cookie.get('addrEth');
                var contract = VotingContract.at(sm_address);
                contract.Dislike({from: addr});
                $scope.stream = title
                $scope.stream.upvotes = contract.totalVotesFor.call().toString();
                $scope.stream.downvotes = contract.totalVotesAgainst.call().toString();
                
                
            }
        }
    });

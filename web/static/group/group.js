web3 = new Web3(new Web3.providers.HttpProvider("http://localhost:8545"));
VotingContract = web3.eth.contract([{"constant":true,"inputs":[],"name":"upVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"Like","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesFor","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":true,"inputs":[],"name":"downVotes","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"view","type":"function"},{"constant":false,"inputs":[],"name":"totalVotesAgainst","outputs":[{"name":"","type":"uint8"}],"payable":false,"stateMutability":"nonpayable","type":"function"},{"constant":false,"inputs":[],"name":"Dislike","outputs":[],"payable":false,"stateMutability":"nonpayable","type":"function"},{"inputs":[],"payable":false,"stateMutability":"nonpayable","type":"constructor"}]);


angular.module('App.group', ['ngRoute', 'ngCookies'])

    .controller('GroupController', function ($scope, $http, $cookies) {

        console.log("GroupController");

        $scope.list_my_group = [];
        $scope.list_to_join_group = [];

        $scope.new_group_tag = null;
        $scope.new_group_name = null;

        $scope.new_post_group_tag = null;
        $scope.new_post_group_title = null;
        $scope.new_post_group_type = null;
        $scope.new_post_group_content = null;
        $scope.new_post_group_image = null;

        $scope.new_member_tag = null;
        $scope.new_member_address = null;

        $scope.join_group_tag = null;

        $scope.current_group = null;
        $scope.current_group_posts = null;

        console.log("GroupController");

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

        $scope.get_my_groups = function () {
            $http.get('/get_my_groups')
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_my_groups");
                        console.log(e.data);
                        $scope.list_my_group = e.data;
                        return e.data;
                    }
                }, function error(e) {
                    console.log("error /get_my_groups");
                    $scope.errors = e.data.errors;
                });
        };

        $scope.get_to_join_groups = function () {
            $http.get('/get_pending_invites')
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_to_join_groups");
                        console.log(e.data);
                        $scope.list_to_join_group = e.data;
                    }
                }, function error(e) {
                    console.log("error /get_to_join_groups");
                    $scope.errors = e.data.errors;
                });
        };

        $scope.createGroup = function () {
            if ($scope.new_group_name != null && $scope.new_group_tag != null) {
                $http.get('/create_group/' + String($scope.new_group_tag) + '/' + String($scope.new_group_name))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /create_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /create_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.new_group_tag = null;
                $scope.new_group_name = null;
            }
        };

        $scope.inviteMember = function () {
            if ($scope.new_member_tag != null && $scope.new_member_address != null) {
                $http.get('/add_to_group/' + String($scope.new_member_address) + '/' + String($scope.new_member_tag))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /add_to_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /add_to_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.new_member_tag = null;
                $scope.new_member_address = null;
            }
        };

        $scope.joinGroup = function () {
            if ($scope.join_group_tag != null) {
                $http.get('/join_group/' + String($scope.join_group_tag))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /join_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /join_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.join_group_tag = null;
            }
        };

        $scope.getGroupPosts = function (group) {
            $http.get('/get_posts/' + String(group))
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_posts/group");
                        for(i=0; i < e.data.length; i++){
                            var sm_address = e.data[i].smartcontract;
                            console.log("listposts");
                            console.log(sm_address);
                            console.log("endlist_post");
                            var contract = VotingContract.at(sm_address);
                            e.data[i].upvotes = contract.totalVotesFor.call().toString();
                            e.data[i].downvotes = contract.totalVotesAgainst.call().toString();
                        }
                        console.log(e.data);
                        $scope.current_group_posts = e.data;
                        return e.data
                        // window.location.href = "#!/home";
                    }
                }, function error(e) {
                    console.log("error /get_posts/group");
                    $scope.errors = e.data.errors;
                    return []
                });
        };

        $scope.upvote = function (stream) {
            var found = $scope.current_group_posts.find(function(element) {
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
            var found = $scope.current_group_posts.find(function(element) {
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

        $scope.get_my_groups();
        $scope.get_to_join_groups();
    });

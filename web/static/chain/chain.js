angular.module('App.chain', ['ngRoute'])

    .controller('ChainController', function ($scope, $http) {
        $scope.current_chain = null;
        $scope.ip_chain = null;
        $scope.port_chain = 1234;
        $scope.name_chain = null;
        $scope.nickname_chain = null;

        console.log("ChainController");

        $scope.connectToChain = function() {
            if ( $scope.ip_chain !== null && $scope.name_chain !== null && $scope.nickname_chain) {
                $http.get('/connect_blockchain/' + String($scope.name_chain) + '/' + String($scope.ip_chain) + '/' + String($scope.port_chain)+'/'+String($scope.nickname_chain))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("/connect_blockchain");
                            console.log(e.data);
                            window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error connect_blockchain");
                        $scope.errors = e.data.errors;
                    });
            }
        };

        $scope.new_chain_name = null;
        $scope.new_chain_nickname = null;

        $scope.createChain = function () {
            if ($scope.new_chain_name !== null && $scope.new_chain_nickname !== null ) {
                $http.get('/create_blockchain/'+String($scope.new_chain_name)+'/'+String($scope.new_chain_nickname))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("/create_blockchain");
                            console.log(e.data);
                            window.location.href = "#!/home";
                        }
                    }, function error(e) {
                            console.log("error create chain");
                            $scope.errors = e.data.errors;
                    });
            }
        };

        $scope.userstate = '';

        var is_user_connected = function () {
            $http.get('/state')
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("/state");
                        $scope.userstate = e.data;
                        // document.getElementById("state_user").innerHTML = e.data;
                        return String(e.data);
                    }
                }, function error(e) {
                    console.log("error isconnected");
                    $scope.errors = e.data.errors;
                    $scope.userstate = "error";
                    return String(e.data);
                });
        };

        is_user_connected();

    });

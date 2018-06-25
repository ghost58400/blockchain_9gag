angular.module('App.chain', ['ngRoute'])

    .controller('ChainController', function ($scope, $http) {
        $scope.current_chain = null;
        $scope.ip_chain = null;
        $scope.port_chain = 1234;
        $scope.name_chain = null;
        $scope.connected = false;
        $scope.nickname_chain = null;

        // $http.get('/connect/chain1/172.17.0.10/1234');

        $scope.connectToChain = function() {
            if ( $scope.ip_chain !== null && $scope.name_chain !== null && $scope.nickname_chain) {
                $http.get('/connect/' + String($scope.name_chain) + '/' + String($scope.ip_chain) + '/' + String($scope.port_chain)+'/'+String($scope.nickname_chain))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '')
                            console.log("/connect");
                        $scope.connected = true;
                        console.log(e.data);
                    }, function error(e) {
                        console.log("error");
                        $scope.errors = e.data.errors;
                    });
            }
        }
    });

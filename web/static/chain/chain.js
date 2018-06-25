angular.module('App.chain', ['ngRoute'])

    .controller('ChainController', function ($scope, $http) {
        $scope.current_chain = null;
        $scope.ip_chain = null;
        $scope.port_chain = 1234;
        $scope.name_chain = null;
        $scope.connected = false;

        // $http.get('/connect/chain1/172.17.0.10/1234');

        $scope.connectToChain = function() {
            $http.get('/connect/'+$scope.name_chain+'/'+$scope.ip_chain+'/'+$scope.port_chain)
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
    });

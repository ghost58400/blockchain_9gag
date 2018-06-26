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
                        if (e.data !== '')
                            console.log("/connect_blockchain");
                        console.log(e.data);
                    }, function error(e) {
                        console.log("error connect_blockchain");
                        $scope.errors = e.data.errors;
                    });
            }
        };

        $scope.userstate = '';

        $scope.is_user_connected = function () {
            // $http.get('/state')
            //     .then(function success(e) {
            //         console.log(e);
            //         $scope.errors = [];
            //         if (e.data !== '') {
            //             console.log("/state");
            //             $scope.userstate = e.data;
            //             console.log($scope.list_stream);
            //         }
            //     }, function error(e) {
            //         console.log("error isconnected");
            //         $scope.errors = e.data.errors;
            //         $scope.userstate = "error";
            //     });
            // return $scope.userstate;
            console.log($http.get('/state'));
            return $http.get('/state');
        }
    });

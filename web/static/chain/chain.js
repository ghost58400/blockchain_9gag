angular.module('App.chain', ['ngRoute'])

    .controller('ChainController', function ($scope, $http) {
        $scope.current_chain = null;
    });

angular.module('App.login', ['ngRoute'])

    .controller('LoginController', function ($scope, $http) {
        $scope.list_user = [];
        $scope.local_user = null;
    });

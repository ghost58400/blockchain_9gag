
angular.module('App', ['ngRoute','App.post',])

//routage
    .config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {

    $locationProvider.hashPrefix('!');

    $routeProvider.otherwise({redirectTo: '/home'});

}]);


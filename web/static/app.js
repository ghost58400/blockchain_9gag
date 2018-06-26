
angular.module('App', ['ngRoute','App.post', 'App.login', 'App.chain',])

//routage
    .config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {

    $locationProvider.hashPrefix('!');

    $routeProvider.otherwise({redirectTo: '/connect_chain'});

}])

.config(['$routeProvider', function ($routeProvider) {
    $routeProvider.when('/connect_chain', {
        templateUrl: 'static/chain/connect_chain.html',
        controller: 'ChainController'
    });
    $routeProvider.when('/create_chain', {
        templateUrl: 'static/chain/create_chain.html',
        controller: 'ChainController'
    });
    $routeProvider.when('/home', {
        templateUrl: 'static/post/all_posts.html',
        controller: 'PostController'
    });
    $routeProvider.when('/create_post', {
        templateUrl: 'static/post/create_post.html',
        controller: 'PostController'
    });
    $routeProvider.when('/show_post', {
        templateUrl: 'static/post/show_post.html',
        controller: 'PostController'
    });
    // $routeProvider.when('/login', {
    //     templateUrl: 'static/login/login.html',
    //     controller: 'LoginController'
    // });
}]);


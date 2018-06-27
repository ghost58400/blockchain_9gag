
angular.module('App', ['ngRoute','App.post', 'App.chain', 'App.group'])

//routage
    .config(['$locationProvider', '$routeProvider', function($locationProvider, $routeProvider) {

    $locationProvider.hashPrefix('!');

    $routeProvider.otherwise({redirectTo: '/home'});

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
    $routeProvider.when('/create_group', {
        templateUrl: 'static/group/create_group.html',
        controller: 'GroupController'
    });
    $routeProvider.when('/invite_group', {
        templateUrl: 'static/group/invite_group.html',
        controller: 'GroupController'
    });
    $routeProvider.when('/join_group', {
        templateUrl: 'static/group/join_group.html',
        controller: 'GroupController'
    });
    $routeProvider.when('/post_group', {
        templateUrl: 'static/group/post_group.html',
        controller: 'GroupController'
    });
}]);


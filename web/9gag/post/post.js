angular.module('App.post', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/login', {
            templateUrl: 'login.html',
            controller: 'LoginController'
        });
        $routeProvider.when('/home', {
            templateUrl: 'post/all_posts.html',
            controller: 'PostController'
        });
        $routeProvider.when('/create_post', {
            templateUrl: 'post/create_post.html',
            controller: 'PostController'
        });
        $routeProvider.when('/show_post', {
            templateUrl: 'post/show_post_html',
            controller: 'PostController'
        });
    }])

    .controller('PostController', function ($scope, $http) {

        $scope.list_posts = [];

    })

    .controller('LoginController', function ($scope, $htpp) {
        $scope.list_user = [];
        $scope.local_user = null;
    });

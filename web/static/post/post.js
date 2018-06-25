angular.module('App.post', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
        $routeProvider.when('/login', {
            templateUrl: 'static/login.html',
            controller: 'LoginController'
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
            templateUrl: 'static/post/show_post_html',
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

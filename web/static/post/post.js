angular.module('App.post', ['ngRoute'])

    .controller('PostController', function ($scope, $http) {

        $scope.list_posts = [];
        $scope.current_post = null;

        $http.get('/get_posts')
            .then(function success(e) {
                $scope.errors = [];
                if (e.data !== '')
                    $scope.list_posts = e.data;
            }, function error(e) {
                $scope.errors = e.data.errors;
            });

        $scope.show_post = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
            }
        };

        $scope.upvote = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
            //    upvote
            }
        };

        $scope.downvote = function (title) {
            var found = $scope.list_posts.find(function(element) {
                return element.title === title;
            });
            if (found) {
                $scope.current_post = found;
             //    downvote
            }
        }
    });

angular.module('App.post', ['ngRoute'])

    .controller('PostController', function ($scope, $http) {

        $scope.list_stream = [];
        $scope.current_post = null;

        $scope.new_post_title = null;
        $scope.new_post_content = null;
        $scope.new_post_type = null;
        $scope.new_post_visibility = null;

        console.log("PostController");

        $http.get('/get_posts')
            .then(function success(e) {
                $scope.errors = [];
                if (e.data !== '')
                    console.log("/get_posts");
                    $scope.list_stream = e.data;
                    console.log($scope.list_stream);
            }, function error(e) {
                console.log("error");
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

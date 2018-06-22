angular.module('App.post', ['ngRoute'])

    .config(['$routeProvider', function ($routeProvider) {
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
        })
    }])

    .controller('PostController', function ($scope, $http) {

        $scope.list_posts = [];

        $http.get('model/item.php?request=all')
            .then(function success(e) {
                $scope.errors = [];
                if (e.data !== '')
                    $scope.list_product = e.data;
            }, function error(e) {
                $scope.errors = e.data.errors;
            });

        $scope.viewProduct = function (id) {
            var found = $scope.list_product.find(function(element) {
                return element.id === id;
            });
            if (found) {
                $scope.productDisplay = found;
            }
            angular.element('#view_product_modal').modal('show');
        };

        $scope.addToCart = function (index) {
            var cart = localStorage.getItem('cart');
            if (cart == null)
                cart = [];
            else
                cart = JSON.parse(cart);

            var item = $scope.list_product[index];

            var found = cart.find(function(element) {
                return element.id === item.id;
            });


            if (found) {
                item.num = found.num + 1;
                cart.splice(cart.indexOf(found), 1);
            }
            else
                item.num = 1;

            cart.push(item);
            localStorage.setItem('cart', JSON.stringify(cart));
        };

    });

angular.module('App.group', ['ngRoute'])

    .controller('GroupController', function ($scope, $http) {

        console.log("GroupController");

        $scope.list_my_group = [];
        $scope.list_to_join_group = [];

        $scope.new_group_tag = null;
        $scope.new_group_name = null;

        $scope.new_post_group_tag = null;
        $scope.new_post_group_title = null;
        $scope.new_post_group_type = null;
        $scope.new_post_group_content = null;
        $scope.new_post_group_image = null;

        $scope.new_member_tag = null;
        $scope.new_member_address = null;

        $scope.join_group_tag = null;

        $scope.current_group = null;
        $scope.current_group_posts = null;

        console.log("GroupController");


        $scope.get_my_groups = function () {
            $http.get('/get_my_groups')
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_my_groups");
                        console.log(e.data);
                        $scope.list_my_group = e.data;
                        return e.data;
                    }
                }, function error(e) {
                    console.log("error /get_my_groups");
                    $scope.errors = e.data.errors;
                });
        };

        $scope.get_to_join_groups = function () {
            $http.get('/get_pending_invites')
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_to_join_groups");
                        console.log(e.data);
                        $scope.list_to_join_group = e.data;
                    }
                }, function error(e) {
                    console.log("error /get_to_join_groups");
                    $scope.errors = e.data.errors;
                });
        };

        $scope.createGroup = function () {
            if ($scope.new_group_name != null && $scope.new_group_tag != null) {
                $http.get('/create_group/' + String($scope.new_group_tag) + '/' + String($scope.new_group_name))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /create_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /create_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.new_group_tag = null;
                $scope.new_group_name = null;
            }
        };

        $scope.inviteMember = function () {
            if ($scope.new_member_tag != null && $scope.new_member_address != null) {
                $http.get('/add_to_group/' + String($scope.new_member_address) + '/' + String($scope.new_member_tag))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /add_to_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /add_to_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.new_member_tag = null;
                $scope.new_member_address = null;
            }
        };

        $scope.joinGroup = function () {
            if ($scope.join_group_tag != null) {
                $http.get('/join_group/' + String($scope.join_group_tag))
                    .then(function success(e) {
                        $scope.errors = [];
                        if (e.data !== '') {
                            console.log("success /join_group");
                            console.log(e.data);
                            // window.location.href = "#!/home";
                        }
                    }, function error(e) {
                        console.log("error /join_group");
                        $scope.errors = e.data.errors;
                    });
                $scope.join_group_tag = null;
            }
        };

        $scope.getGroupPosts = function (group) {
            $http.get('/get_posts/' + String(group))
                .then(function success(e) {
                    $scope.errors = [];
                    if (e.data !== '') {
                        console.log("success /get_posts/group");
                        console.log(e.data);
                        $scope.current_group_posts = e.data;
                        return e.data
                        // window.location.href = "#!/home";
                    }
                }, function error(e) {
                    console.log("error /get_posts/group");
                    $scope.errors = e.data.errors;
                    return []
                });
        };



        $scope.get_my_groups();
        $scope.get_to_join_groups();
    });

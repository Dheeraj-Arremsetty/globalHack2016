app.controller('optionsSelectControler', function($scope, $http, $location) {
    $scope.getFoodData = function(loginInfo) {
        $scope.waitingForLogin = true;
        $http.post(
            $scope.loginUrl,
            {
            },
            { cors: true }
            )
            .then(function (resp) {
                // Success
                //$scope.$storage.token = resp.data.token;
            alert(JSON.stringify(resp.data));
                $scope.foodData = resp.data;
//                $scope.loggedInEmployeeId = loginInfo.employeeId;
//                $scope.clearLoginForm();
//                $location.path('/main')
            //debugger;
            $location.url("/#/foodPage");
            },
            function (resp) {
                // Failure
                $scope.clearLoginForm();
                //alert("Login failed");
            });


    }


    $scope.$storage = $scope.$parent.$storage;
    $scope.loginUrl = '/food';
    $scope.waitingForLogin = false;

});
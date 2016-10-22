// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('loginController', function($scope, $http, $location) {
    $scope.submitLogin = function(loginInfo) {
        $scope.waitingForLogin = true;
        $http.post(
            $scope.loginUrl, 
            { 
                username: loginInfo.username, 
                password: loginInfo.password, 
                grant_type: 'password' 
            },
            { cors: true }
            )
            .then(function (resp) {
                // Success
                $scope.$storage.token = resp.data.token;
                $scope.loggedInEmployeeId = loginInfo.employeeId;
                $scope.clearLoginForm();
                $location.path('/main')
            },
            function (resp) {
                // Failure
                $scope.clearLoginForm();
                alert("Login failed");
            });

    }
    
    $scope.clearLoginForm = function () {
        $scope.login.employeeId = "";
        $scope.login.password = "";
        $scope.waitingForLogin = false;
    }

    
    $scope.canSubmitLogin = function() {
        if (!$scope.login) return false;
        return $scope.login.username && $scope.login.password && !$scope.waitingForLogin;
    }
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.loginUrl = '/login';
    $scope.waitingForLogin = false;
 
});
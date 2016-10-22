// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('master', function($scope, $http, $localStorage, $q) {
    $scope.get = function (url) {
        return $scope.$storage.token ? httpGetWithAuth(url) : $http.get(url);
    };
    
    $scope.post = function(url, data) {
        return $scope.$storage.token ? httpPostWithAuth(url, data) : $http.post(url, data);
    }
    
    $scope.login(loginInfo) {
        $http.post(
            $scope.loginUrl, 
            { 
                username: loginInfo.username, password: loginInfo.password, grant_type: 'password' }
            )
            .then(function (resp) {
                // Success
                $scope.$storage.token = resp.data.access_token;
                $scope.loggedInEmployeeId = loginInfo.employeeId;
                $scope.clearLoginForm();
            },
            function (resp) {
                // Failure
                $scope.clearLoginForm();
                alert("Login failed");
            });

    }
    
    function httpGetWithAuth(url) {
        return httpRequestWithAuth('get', url);
    }
    
    function httpPostWithAuth(url, data) {
        return httpRequestWithAuth('post', url, data);
    }
    
    function httpRequestWithAuth(method, url, data) {
        return $http[method](url, data)
            .catch(function(resp) {
                if (resp.status === 401) {
                    // Not authenticated, or authentication expired. Token is not valid.

                    alert('Login session has expired. Please enter your credentials.');

                    // Kill the stored token (don't call $scope.logout because there's no need
                    // to send a logout request to the server).
                    delete $scope.$storage.token;

                    // Return an empty object just to appease anything that might be waiting on
                    // the results of this call.
                    return {};
                } else {
                    // Request failed for some reason other than lack of authentication. 
                    // Pass the failure on.
                    return $q.reject(resp);
                }
        });
    }
    
    $scope.$storage = $localStorage;
    $scope.loginUrl = '/Login';
 
});
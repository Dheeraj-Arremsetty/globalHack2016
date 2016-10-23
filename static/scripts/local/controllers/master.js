// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('master', function($scope, $http, $localStorage, $q) {
    $scope.get = function (url) {
        return $scope.$storage.token ? httpGetWithAuth(url) : $http.get(url);
    };
    
    $scope.post = function(url, data) {
        return $scope.$storage.token ? $http.post(url, data, getAuthConfig()) : $http.post(url, data);
    }
    
    $scope.put = function(url, data) {
        return $scope.$storage.token ? $http.put(url, data, getAuthConfig()) : $http.put(url, data);
    }
    
    function httpGetWithAuth(url) {
        return $http.get(url, getAuthConfig())
            .catch(function(resp) {
                if (resp.status === 401) {
                    // Not authenticated, or authentication expired. Token is not valid.

                    alert('Login session has expired. Please enter your credentials.');

                    // Kill the stored token.
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
    
    
    function getAuthConfig() {
        return {
            headers: {
                Authorization: 'Bearer ' + $scope.$storage.token
            }
        };
    }

    
    function httpRequestWithAuth(method, url, data) {
        return $http[method](url, data)
            .catch(function(resp) {
                if (resp.status === 401) {
                    // Not authenticated, or authentication expired. Token is not valid.

                    alert('Login session has expired. Please enter your credentials.');

                    // Kill the stored token.
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
    
    $scope.volCount = '(Still Counting)';
    $scope.connCount = '(Still Counting)';
    
    $http.get('/counters/volunteers').then(function(resp) {
        $scope.volCount = resp.data.count;
    });
    
    $http.get('/counters/connections').then(function(resp) {
        $scope.connCount = resp.data.count;
    });
    
 
});
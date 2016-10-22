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
 
});
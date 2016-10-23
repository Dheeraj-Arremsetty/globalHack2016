// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('counterController', function($scope, $http) {
    $scope.volCount = '(Still Counting)';
    $scope.connCount = '(Still Counting)';
    
    $http.get('/counters/volunteers').then(function(resp) {
        $scope.volCount = resp.data.count;
    });
    
    $http.get('/counters/connections').then(function(resp) {
        $scope.connCount = resp.data.count;
    })
    
    
 
});
// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('providerController', function($scope) {
    $scope.updateProviderInfo = function() {
        $scope.get('/provider?provider_id=' + $scope.$storage.token)
            .then(function(resp) {
                $scope.providerInfo = resp.data[0];
            })
            .catch(function(resp) {
                $scope.providerInfo = { Error: 'There was a problem retrieving the information.' };
        })
    };
    
        $scope.getAllNeeds = function() {
        $scope.get('/needs')
            .then(function(resp) {
                $scope.allNeeds = resp.data.result;
        });
    }
    
    $scope.sendProviderInfo = function() {};
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
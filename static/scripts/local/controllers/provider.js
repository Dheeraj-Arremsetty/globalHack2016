// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('providerController', function($scope) {
    $scope.updateProviderInfo = function() {
        alert('Fetching provider info');
        $scope.get('/provider')
            .then(function(resp) {
                $scope.providerInfo = resp.data;
            })
            .catch(function(resp) {
                $scope.providerInfo = { Error: 'There was a problem retrieving the information.' };
        })
    };
 
});
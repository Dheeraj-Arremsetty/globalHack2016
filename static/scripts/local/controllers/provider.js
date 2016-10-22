// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('providerController', function($scope) {
    $scope.updateProviderInfo = function() {
        $scope.get('/provider?provider_id=' + $scope.$storage.token)
            .then(function(resp) {
                // $scope.providerInfo = resp.data[0];
                $scope.providerInfo = {
                    name: 'John Smith',
                    street_address: '123 Main St',
                    city: 'nowhere',
                    state: 'MM',
                    zip_code: '99999',
                    description: 'Lorem ipsom dolor sic amet'
                    needs: {
                        food: {
                            type: 'stuff',
                            number_of_meals: '3',
                            expiration: '2016-10-25'
                        }
                    }
                }
            })
            .catch(function(resp) {
                $scope.providerInfo = { Error: 'There was a problem retrieving the information.' };
        })
    };
    
        $scope.getAllNeeds = function() {
//            $scope.get('/needs')
//                .then(function(resp) {
//                    $scope.allNeeds = resp.data.result;
//            });
            $acope.allNeeds = {
                food: ['type', 'number_of_meals', 'expiration'],
                beds: ['count'],
                training: ['topics', 'hours']
            }
    }
        
        $scope.getClassForNeed(need) {
            return $scope.providerInfo.needs[need].offered ? 'selected' : 'unselected';
        }
    
    $scope.sendProviderInfo = function() {};
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
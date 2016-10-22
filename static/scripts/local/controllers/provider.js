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
                    description: 'Lorem ipsom dolor sic amet',
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
        });
    };
    
        $scope.getAllNeeds = function() {
//            $scope.get('/needs')
//                .then(function(resp) {
//                    $scope.allNeeds = resp.data.result;
//            });
            $scope.allNeeds = [
                {
                    name: 'food',
                    attributes: ['type', 'number_of_meals', 'expiration']
                },
                {
                    name: 'beds',
                    attributes: ['count']
                },
                {
                    name: 'training',
                    attributes: ['topics', 'hours']
                }
            ]
    };
        
    $scope.getClassForNeed = function(need) {
        var isOffered = need && $scope.providerInfo && $scope.providerInfo.needs && $scope.providerInfo.needs[need]
        return isOffered ? 'selected' : 'unselected';
    }
    
    $scope.sendProviderInfo = function() {};
    
    $scope.showNeedFlyout = function(need) {
        for (var i = 0; i < $scope.allNeeds.length; i++) {
            $scope['flyoutShown' + need] = ($scope.allNeeds[i].name === need);
        }
    }
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
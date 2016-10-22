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
    
    $scope.isNeedSelected = function(need) {
        return !!(need && $scope.providerInfo && $scope.providerInfo.needs && $scope.providerInfo.needs[need]);
    }
        
    $scope.getClassForNeed = function(need) {
        return $scope.isNeedSelected(need) ? 'selected' : 'unselected';
    }
    
    $scope.sendProviderInfo = function() {};
    
    $scope.submitProviderNeeds = function() {};
    
    $scope.showNeedFlyout = function(need) {
        for (var i = 0; i < $scope.allNeeds.length; i++) {
            var currentNeed = $scope.allNeeds[i].name
            $scope['flyoutShown' + currentNeed] = (currentNeed === need);
        }
    }
    
    $scope.toggleNeedSelection = function(need) {
        if ($scope.isNeedSelected(need)) {
            if (!$scope.backupNeedSelections) {
                $scope.backupNeedSelections = {};
            }
            $scope.backupNeedSelections[need] = $scope.providerInfo.needs[need];
            delete $scope.providerInfo.needs[need];
            $scope['flyoutShown' + need] = false;
        } else {
            if ($scope.backupNeedSelections && $scope.backupNeedSelections[need]) {
                $scope.providerInfo.needs[need] = $scope.backupNeedSelections[need];
            } else {
                $scope.providerInfo.needs[need] = {};
            }
        }
    }
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
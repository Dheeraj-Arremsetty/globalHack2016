// Master Angular controller
// Must include app.js, ex:
// <script src="/scripts/local/app.js" />

app.controller('providerController', function($scope) {
    $scope.updateProviderInfo = function() {
        $scope.get('/provider?provider_id=' + $scope.$storage.token)
            .then(function(resp) {
                if (resp.data && resp.data[0]) {
                   $scope.providerInfo = resp.data[0]; 
                } else {
                    $scope.providerInfo = { };
                }
                
                $scope.needs = $scope.providerInfo.needs || {};
                for (key in $scope.needs) {
                    for (attr in $scope.needs[key]) {
                        $scope.needAttrs[key][attr] = $scope.needs[key][attr];
                    }
                }
                
            })
            .catch(function(resp) {
                $scope.providerInfo = { Error: 'There was a problem retrieving the information.' };
        });
    };
    
        $scope.getAllNeeds = function() {
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
        return !!(need && $scope.needs && $scope.needs.hasOwnProperty(need));
    }
        
    $scope.getClassForNeed = function(need) {
        return $scope.isNeedSelected(need) ? 'selected' : 'unselected';
    }
    
    $scope.sendProviderInfo = function() {
        var providerWithoutNeeds = {};
        for (var key in $scope.providerInfo) {
            if (key === 'needs') continue;
            providerWithoutNeeds[key] = $scope.providerInfo[key];
        }
        var body = {
            user_id: $scope.$storage.token,
            info: providerWithoutNeeds
        };
        
        $scope.put($scope.infoUpdateUrl, body)
            .then(function(resp) {
            alert('Success');
        })
            .catch(function(resp) {
            alert('Something went wrong');
        });
    };
    
    $scope.submitProviderNeeds = function() {
        var consolidatedNeeds = {};
        for (var needKey in $scope.needs) {
            if ($scope.needs[needKey]) {
                consolidatedNeeds[needKey] = {};
                for (attrKey in $scope.needAttrs[needKey]) {
                    consolidatedNeeds[needKey][attrKey] = $scope.needAttrs[needKey][attrKey];
                }
            }
        }
        
        var body = {
            user_id: $scope.$storage.token,
            needs: consolidatedNeeds
        }
        
        $scope.put($scope.needsUpdateUrl, body)
            .then(function(resp) {
            alert('Success');
        })
            .catch(function(resp) {
            alert('Something went wrong');
        });
    };
    
    $scope.showNeedFlyout = function(need) {
        for (var i = 0; i < $scope.allNeeds.length; i++) {
            var currentNeed = $scope.allNeeds[i].name
            $scope['flyoutShown' + currentNeed] = (currentNeed === need);
        }
    }
    
    $scope.toggleNeedSelection = function(need) {
        if ($scope.isNeedSelected(need)) {
            delete $scope.needs[need];
            $scope['flyoutShown' + need] = false;
        } else {
            $scope.needs[need] = true;
            $scope.showNeedFlyout(need);
        }
    }
    
    $scope.needAttrs = {food: {}, beds: {}, training: {}};
    $scope.$storage = $scope.$parent.$storage;
    $scope.infoUpdateUrl = '/providers/info';
    $scope.needsUpdateUrl = '/providers/needs';
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
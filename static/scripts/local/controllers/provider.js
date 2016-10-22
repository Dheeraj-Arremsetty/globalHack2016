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
                    $scope.providerInfo = { needs: { food: {}, beds: {}, training{} } };
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
        return !!(need && $scope.providerInfo && $scope.providerInfo.needs && $scope.providerInfo.needs[need]);
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
            
            var needAttrs = $scope.providerInfo.needs[need];
            var emptyAttributes = !needAttrs;
            if (!emptyAttributes) {
                emptyAttributes = true;
                for (var attr in needAttrs) {
                    if (needAttrs[attr]) {
                        emptyAttributes = false;
                        break;
                    } else alert(attr + ': ' + needAttrs[attr]);
                }
            }
            if (emptyAttributes) $scope.showNeedFlyout(need);
        }
    }
    
    $scope.$storage = $scope.$parent.$storage;
    $scope.infoUpdateUrl = '/providers/info';
    $scope.needsUpdateUrl = '/providers/needs';
    $scope.getAllNeeds();
    $scope.updateProviderInfo();
 
});
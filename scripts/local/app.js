// Must include angular and ngStorage, ex.:
// <script src="https://ajax.googleapis.com/ajax/libs/angularjs/1.5.8/angular.min.js" />
// <script src="https://cdnjs.cloudflare.com/ajax/libs/ngStorage/0.3.6/ngStorage.min.js" />

var app = angular.module('mainApp', ['ngStorage'],
    function ($httpProvider) {
    // Code to make POST requests use url-encoded string instead of JSON
    // from http://victorblog.com/2012/12/20/make-angularjs-http-service-behave-like-jquery-ajax/


    // Use x-www-form-urlencoded Content-Type
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded;charset=utf-8';

    /**
    * The workhorse; converts an object to x-www-form-urlencoded serialization.
    * @param {Object} obj
    * @return {String}
    */ 
    var param = function(obj) {
    var query = '', name, value, fullSubName, subName, subValue, innerObj, i;
      
    for(name in obj) {
        value = obj[name];
        
        if(value instanceof Array) {
            for(i=0; i<value.length; ++i) {
                subValue = value[i];
                fullSubName = name + '[' + i + ']';
                innerObj = {};
                innerObj[fullSubName] = subValue;
                query += param(innerObj) + '&';
            }
        }
        else if(value instanceof Object) {
        for(subName in value) {
            subValue = value[subName];
            fullSubName = name + '[' + subName + ']';
            innerObj = {};
            innerObj[fullSubName] = subValue;
            query += param(innerObj) + '&';
        }
        }
        else if(value !== undefined && value !== null)
        query += encodeURIComponent(name) + '=' + encodeURIComponent(value) + '&';
    }
      
    return query.length ? query.substr(0, query.length - 1) : query;
    };

    // Override $http service's default transformRequest
    $httpProvider.defaults.transformRequest = [function(data) {
    return angular.isObject(data) && String(data) !== '[object File]' ? param(data) : data;
    }];
});

    

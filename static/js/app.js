angular.module('livia', []).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/', {templateUrl: 'partials/admin.html', controller: NavController}).
      when('/loggers', {templateUrl: 'partials/loggers.html', controller: LoggersController}).
      when('/loggers/new', {templateUrl: 'partials/loggers-new.html', controller: LoggersController}).
      when('/data', {templateUrl: 'partials/data.html', controller: NavController}).
      otherwise({redirectTo: '/'});
}]);

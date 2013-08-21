angular.module('livia', []).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/', {templateUrl: 'partials/admin.html', controller: LiviaController}).
      when('/loggers', {templateUrl: 'partials/loggers.html', controller: LiviaController}).
      when('/data', {templateUrl: 'partials/data.html', controller: LiviaController}).
      otherwise({redirectTo: '/'});
}]);

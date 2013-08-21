angular.module('livia', []).
  config(['$routeProvider', function($routeProvider) {
  $routeProvider.
      when('/', {templateUrl: 'partials/login.html', controller: LiviaController}).
      otherwise({redirectTo: '/'});
}]);

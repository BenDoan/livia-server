function NavController($scope, $http, $route, $location, $routeParams){
   $scope.$location = $location;
}

function LoggersController($scope, $http){
    $http.get('/loggers').then(function(loggers){
        $scope.loggers = loggers.data;
    });
    $scope.hello = "hi";
}


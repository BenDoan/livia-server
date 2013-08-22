function NavController($scope, $http, $route, $location, $routeParams){
   $scope.$location = $location;
}

function LoggersController($scope, $http){
    $http.get('/loggers').then(function(loggers){
        $scope.loggers = loggers.data;
    });
    $scope.hello = "hi";
}

function DataController($scope, $http){
    $http.get('/projects').then(function(projects){
        $scope.projects = projects.data;
        for(project in projects){
            $http.get('/loggers'
    });
    $scope.hello = "hi";
}

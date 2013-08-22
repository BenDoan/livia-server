function NavController($scope, $http, $route, $location, $routeParams){
   $scope.$location = $location;
}

function LoggersController($scope, $http, $location){
    $http.get('/loggers').then(function(loggers){
        $scope.loggers = loggers.data.reverse();
    });

    $scope.add = function(){
        $http.get('/projects/' + $scope.logger.project + '/addlogger?description=' + $scope.logger.description).then(function(id){
            $location.path('/loggers')
        });
    };
}
function DataController($scope, $http, $location){
    $http.get('/data/').then(function(data){
        $scope.data=data.data;
    });
}

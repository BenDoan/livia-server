function NavController($scope, $http, $route, $location, $routeParams){
   $scope.$location = $location;
}

function LoggersController($scope, $http, $location){
    $http.get('/loggers').then(function(loggers){
        $scope.loggers = loggers.data.reverse();
    });
    $scope.predicate = 'id';
    $scope.reverse = true;

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
    $scope.hasData = function(logger){
        return logger.data.length!=0;
    };
    $scope.truncate = function(str,l){
        if(str.length>l){
            return str.slice(1,l-3)+"...";
        }
        return str;
    };
}

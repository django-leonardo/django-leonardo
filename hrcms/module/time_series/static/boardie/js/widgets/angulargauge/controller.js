app.controller("angulargaugeCtrl", ["$scope", function($scope) {

  if (!$scope.widget.uid) {
    _.extend($scope.widget, $.widget_defaults[$scope.widget.kind]);
  }

  $scope.widget_options = $.widget_options;

}]);
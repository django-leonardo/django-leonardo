app.directive("angulargauge", ["WidgetModel", function(WidgetModel) {

  var linkFn = function(scope, element, attrs) {

    var loaded = {};
    var gauge = {};

    function onSuccess(data) {
      if(loaded[scope.widget.uid]) {
        gauge[scope.widget.uid].redraw(data.value, data.unit);
      }
      else {

        var config = {
          min: scope.widget.low_horizon,
          max: scope.widget.high_horizon,
          label: scope.widget.name,
          width: calcWidth(),
          height: calcHeight(),
          majorTicks: scope.widget.major_ticks,
          minorTicks: scope.widget.minor_ticks
        }
        config.redZones = [];
        config.redZones.push({ from: scope.widget.threshold_critical, to: scope.widget.high_horizon });

        config.yellowZones = [];
        config.yellowZones.push({ from: scope.widget.threshold_warning, to: (scope.widget.threshold_critical) });

        config.greenZones = [];
        config.greenZones.push({ from: scope.widget.low_horizon, to: scope.widget.threshold_warning });

        console.log(config);
        loaded[scope.widget.uid] = true;
        gauge[scope.widget.uid] = AngularGauge(scope.widget.uid, config);
        gauge[scope.widget.uid].redraw(data.value, data.unit);
      }
    }

    function update() {
      return WidgetModel.getData(scope.widget).success(onSuccess);
    }

    function calcHeight() {
      whole = element.parent().parent();
      whole_height = whole.height();
      header = whole.find("div.widget-header");
      header_height = header.height();
      content_height = whole_height - header_height;
      return content_height - 20;
    }

    function calcWidth() {
      whole = element.parent().parent();
      whole_width = whole.width();
      return whole_width - 20;
    } 

    scope.init(update);

    /*
    scope.$watch("data.value", function(newValue, oldValue) {
      knob.val(newValue).trigger("change");
    });

    scope.$watch("data.min", function(newValue, oldValue) {
      knob.trigger("configure", { min: newValue });
    });

    scope.$watch("data.max", function(newValue, oldValue) {
      knob.trigger("configure", { max: newValue });
    });
    */
  };

  return {
    template: $("#templates-widget-angulargauge-view").html(),
    link: linkFn
  };
}]);
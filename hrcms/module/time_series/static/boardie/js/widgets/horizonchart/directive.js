app.directive("horizonchart", ["WidgetModel","$rootScope", function(WidgetModel,$rootScope) {

  var loaded = {};

  var linkFn = function(scope, element, attrs) {

    function onSuccess(data) {
      data.height = calcHeight() - 32;
      element.find('.horizonchart').height(data.height);
      if(!loaded[scope.widget.uid]) {
        initGraph('#'+scope.widget.uid, data); 
        loaded[scope.widget.uid] = true;
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
      return content_height;
    }

    function calcWidth() {
      whole = element.parent().parent();
      whole_width = whole.width();
      return whole_width;
    }

    function initGraph(placeholder, data) {
      var width = calcWidth();
      var metrics = [];
      var horizon_height = Math.floor(data.height/data.metrics.length)-1;
      var horizon_colors = [].concat($rootScope.colors.positive.slice(0,scope.widget.horizon_folds)).concat($rootScope.colors.negative.slice(0,scope.widget.horizon_folds));
      console.log(horizon_colors);
      var axis_ticks = Math.floor(width/50);

      var context = cubism.context()
        .serverDelay(1000)
        .clientDelay(1000)
        .step(data.step_seconds*1000)
        .size(width);

      var rule = context.rule();
      var graphite = context.graphite(data.host);

      data.metrics.forEach(function (datum) {
        metric = graphite.metric(datum.target).alias(datum.name);
        metrics.push(metric);
      });

      d3.select(placeholder).call(function(div) {

        div.selectAll(".axis")
          .data(["top"])
          .enter().append("div")
          .attr("class", function(d) { return d + " axis"; })
          .each(function(d) { 
            d3.select(this).call(context.axis().ticks(axis_ticks).orient(d)); 
          });

        div.selectAll(".horizon")
          .data(metrics)
          .enter().append("div")
          .attr("class", "horizon")
          .call(context.horizon()
//            .extent([data.low_horizon, data.high_horizon])
            .colors(horizon_colors)
            .height(horizon_height));

        div.select(placeholder).append("div")
          .attr("class", "rule")
          .call(rule);

      });

      /*
      // moving value
      context.on("focus", function(i) {
        d3.selectAll(".value").style("right", i == null ? null : context.size() - i + "px");
      });
      */
    }

    scope.init(update);

    scope.$watch("config.width", function(newValue, oldValue) {
      if (newValue !== oldValue) {
        element.width(calcWidth());
        scope.init(update);
      }
    });

    scope.$watch("config.height", function(newValue, oldValue) {
      if (newValue !== oldValue) {
        element.height(calcHeight());
        scope.init(update);
      }
    });
    
  };

  return {
    template: $("#templates-widget-horizonchart-view").html(),
    link: linkFn
  };

}]);
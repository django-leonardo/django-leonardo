app.directive("areachart", ["WidgetModel", function(WidgetModel) {

  var loaded = {};
  var charts = {};

  var metrics = {};
  var total_metrics = {};

  var linkFn = function(scope, element, attrs) {

    function onSuccess(data) {
      data.height = calcHeight();
      element.height(calcHeight());
      element.width(calcWidth());
      element.find('svg').css('height', calcHeight());
      element.find('svg').css('width', calcWidth());
      //Flotr.draw(element[0], FlotrGraphHelper.transformSeriesOfDatapoints(data, scope.widget, currentColors), FlotrGraphHelper.defaultOptions(scope.widget));
      total_metrics[scope.widget.uid] = data.metrics.length;
      if(!loaded[scope.widget.uid]) {
        metrics[scope.widget.uid] = [];
        initData('#'+scope.widget.uid, data); 
        loaded[scope.widget.uid] = true;
      }
    }

    function addMetric(data) {
      if (data.length > 0) {
        points = []
        data[0].datapoints.forEach(function (point) {
          points.push([point[1]*1000, point[0]]);
        });
        line = {
          key: data[0].target,
          values: points
        }

      }
      else {
        total_metrics[scope.widget.uid] -= 1;
      }
      metrics[scope.widget.uid].push(line);
      if(metrics[scope.widget.uid].length == total_metrics[scope.widget.uid]) {
        console.log(metrics[scope.widget.uid]);
        charts[scope.widget.uid] = initGraph('#'+scope.widget.uid, metrics[scope.widget.uid]); 
      }
      return true;
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

    function initData(placeholder, data) {
      var step = data.step_seconds * 1000;
      var fun = data.step_fun;

      data.metrics.forEach(function (datum) {
        var target = datum.target;
        var host = data.host;
        var start = data.start;
        var end = data.end;

        if (step !== 1e4) target = "summarize(" + target + ",'"
          + (!(step % 36e5) ? step / 36e5 + "hour" : !(step % 6e4) ? step / 6e4 + "min" : step / 1e3 + "sec")
          + "','" + fun + "')";

        var url = host + "/render?format=json"
          + "&target=" + encodeURIComponent("alias(" + target + ",'"+datum.name+"')")
          + "&from=" + start // - 2 * step // off-by-two?
          + "&until=" + end;

        d3.json(url, function(json) {
          if (!json) return callback(new Error("unable to load data"));
          addMetric(json);
        });

      });
    }

    function initGraph(placeholder, chart_metrics) {

      var chart_wrapper = nv.addGraph(function() {
        var chart = nv.models.stackedAreaChart()
          .x(function(d) { return d[0] })
          .y(function(d) { return d[1] })
          .clipEdge(true);

        chart.xAxis
          .showMaxMin(false)
          .tickFormat(function(d) { 
            return d3.time.format('%x')(new Date(d))
          });

        chart.yAxis
          .tickFormat(d3.format(',.2f'));

        d3.select(placeholder+' svg')
          .datum(chart_metrics).call(chart);
        //  .transition().duration(500).call(chart);

        nv.utils.windowResize(chart.update);

        return chart;
      });

      return chart_wrapper;
    }

    scope.init(update);
    
  };

  return {
    template: $("#templates-widget-areachart-view").html(),
    link: linkFn
  };
}]);
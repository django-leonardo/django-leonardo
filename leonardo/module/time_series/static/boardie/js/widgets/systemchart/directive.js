app.directive("systemchart", ["WidgetModel", function(WidgetModel) {

  var loaded = {};
  var systems = {};

  var metrics = {};
  var total_metrics = {};

  var linkFn = function(scope, element, attrs) {

    var loaded = {};
    var chart = {};

    function onSuccess(data) {
      var height = calcHeight();
      var width = calcWidth();

      element.height(height);
      element.width(width);
      element.find('div.systemchart').height(height);
      element.find('div.systemchart').width(width);
      element.find('object').css('height', height);

      if(loaded[scope.widget.uid]) {
          data.forEach(function (datum) {
            if (datum.value == null) {
              var value = 'N/A';
            }
            else {
              var value = datum.value.toFixed(1)
            }
            if(datum.type == 'angulargauge') {
              chart[scope.widget.uid][datum.device].redraw(value, datum.unit);
            }
            if (datum.type == 'number') {
              chart[scope.widget.uid][datum.device].html(value+' '+datum.unit);
            }
            if (datum.type == "boolean") {
              if (datum.value == 0) {
                chart[scope.widget.uid][datum.device].css('background-color', 'red');
              }
              else {
                chart[scope.widget.uid][datum.device].css('background-color', 'green');
              }
            }
          });

      }
      else {
        chart[scope.widget.uid] = {};
        console.log(data);
        data.forEach(function (datum) {
          if (datum.value == null) {
            var value = 'N/A';
          }
          else {
            var value = datum.value.toFixed(1)
          }
          element.find('div.systemchart').append('<div id="device'+scope.widget.uid+datum.device+'" class="device '+datum.type+'"></div>');
          if(datum.type == 'angulargauge') {
            var config = {
              min: scope.widget.low_horizon,
              max: scope.widget.high_horizon,
              label: datum.name,
              width: calcWidth()/11.5,
              height: calcHeight()/11.5,
              majorTicks: scope.widget.major_ticks,
              minorTicks: scope.widget.minor_ticks
            }
            gauge_wrapper = element.find('#device'+scope.widget.uid+datum.device);
            gauge_wrapper.css('top', datum.y + '%');
            gauge_wrapper.css('left', datum.x + '%');

            var gauge = AngularGauge(gauge_wrapper.attr('id'), config);
            gauge.redraw(value, datum.unit);
            chart[scope.widget.uid][datum.device] = gauge;
            
          }
          if(datum.type == 'number') {
            counter = element.find('#device'+scope.widget.uid+datum.device);
            counter.css('top', datum.y + '%');
            counter.css('left', datum.x + '%');
            counter.html(value+' '+datum.unit);
            chart[scope.widget.uid][datum.device] = counter;
          }
          if (datum.type == 'boolean') {
            boolean_wrapper = element.find('#device'+scope.widget.uid+datum.device);
            boolean_wrapper.css('top', datum.y + '%');
            boolean_wrapper.css('left', datum.x + '%');
            // boolean_wrapper.css('height', calcHeight()/11.5);
            // boolean_wrapper.css('width', calcWidth()/11.5);
            if (datum.value == 0) {
              boolean_wrapper.css('background-color', 'red');
            } else {
              boolean_wrapper.css('background-color', 'green');
            }
            addLabel('#device'+scope.widget.uid+datum.device, datum.name);
            chart[scope.widget.uid][datum.device] = boolean_wrapper; 
          }   
          if (datum.type == 'sparkline') {
            height = 30;
            width = calcWidth()/3;
            sparkline = element.find('#device'+scope.widget.uid+datum.device);
            sparkline.css('top', datum.y + '%');
            sparkline.css('left', datum.x + '%');
            sparkline.css('height', height);
            sparkline.css('width', width);
            fake_data = [3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 2, 7, 5, 2, 1, 3, 8, 9, 2, 5, 9, 3, 6, 2, 7, 5, 2, 1, 3, 8, 9, 2, 9];
            var config = {
              "id": '#device'+datum.device,
              "height": height,
              "width": width,
              "interpolation": "basis",
              "animate": true,
              "updateDelay": 1000,
              "transitionDelay": 1000,
              "stroke": "steelblue",
              "stroke-width": 1,
              "fill": "none"
            }
            addLabel('#device'+datum.device, datum.name);
            var spark = displaySparkline(config, fake_data);
            chart[scope.widget.uid][datum.device] = spark; 
          }     
        });
        loaded[scope.widget.uid] = true;
      }
    }
    function addLabel(id, label) {
      el = element.find(id);
      lab = label.split(" ")
      if (typeof lab[1] == "undefined") {
        label = "<span id=" + id + "label"+">" + lab[0] + "</span>";  
      } else {
        label = "<span id=" + id + "label"+">" + lab[1] + "</span>";
      }
      el.append(label);
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
  };

  return {
    template: $("#templates-widget-systemchart-view").html(),
    link: linkFn
  };
}]);
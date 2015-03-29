app.directive("calendarheatmap", ["WidgetModel", function(WidgetModel) {

  var loaded = {};
  var maps = {};

  var linkFn = function(scope, element, attrs) {

    function onSuccess(data) {
      if(loaded[scope.widget.uid]) {
        maps[scope.widget.uid].update(data.values);
      }
      else {
        element.find('#'+scope.widget.uid).css('overflow', 'hidden');

        loaded[scope.widget.uid] = true;

        var map_options = {
          itemSelector: '#'+scope.widget.uid,
          start: new Date(data.start*1000),
          domain: scope.widget.domain,
          subDomain: scope.widget.subdomain,
          range: scope.widget.domain_range,
          data: data.values
        }
        maps[scope.widget.uid] = new CalHeatMap();
        maps[scope.widget.uid].init(map_options);
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

    scope.init(update);

  };

  return {
    template: $("#templates-widget-calendarheatmap-view").html(),
    link: linkFn
  };
}]);
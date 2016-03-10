/* Functions for element resize detection

Example usage: $( element ).widthChanged( someFunction ); - test width 
Example usage: $( element ).heightChanged( someFunction ); - test height
Example usage: $( element ).sizeChanged( someFunction ); - test both */

(function ($) {

$.fn.widthChanged = function (handleFunction) {
    var element = this;
    var lastWidth = element.width();

    setInterval(function () {
        if (lastWidth === element.width()) {
            return;
        }
        if (typeof (handleFunction) == 'function') {
            handleFunction({ width: lastWidth },
                           { width: element.width()});
            lastWidth = element.width();
        }
    }, 100);

    return element;
};

}(jQuery));

(function ($) {

$.fn.heightChanged = function (handleFunction) {
    var element = this;
    var lastHeight = element.height();

    setInterval(function () {
        if (lastHeight === element.height()) {
            return;
        }
        if (typeof (handleFunction) == 'function') {
            handleFunction({ height: lastHeight },
                           { height: element.height() });
            lastHeight = element.height();
        }
    }, 100);

    return element;
};

}(jQuery));

(function ($) {

$.fn.sizeChanged = function (handleFunction) {
    var element = this;
    var lastWidth = element.width();
    var lastHeight = element.height();

    setInterval(function () {
        if (lastWidth === element.width()&&lastHeight === element.height())
            return;
        if (typeof (handleFunction) == 'function') {
            handleFunction({ width: lastWidth, height: lastHeight },
                           { width: element.width(), height: element.height() });
            lastWidth = element.width();
            lastHeight = element.height();
        }
    }, 100);


    return element;
};

}(jQuery));


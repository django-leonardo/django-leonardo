// jQuery for page scrolling feature - requires jQuery Easing plugin
$(function() {
    $('a.page-scroll').bind('click', function(event) {
        var $anchor = $(this);
        $('html, body').stop().animate({
            scrollTop: ($($anchor.attr('href').replace("/", "")).offset().top - 1)
        }, 1500, 'easeInOutExpo');
        event.preventDefault();
    });
});
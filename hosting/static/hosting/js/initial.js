// also declared in datacenterlight/js/main.js
function _initNavUrl() {
    $('.url').click(function(event) {
        event.preventDefault();
        var href = $(this).attr('href');
        $('.navbar-collapse').removeClass('in');
        $('.navbar-collapse').addClass('collapsing');
        if ($(href).length) {
            $('html, body').animate({
                scrollTop: $(href).offset().top
            }, 1000);
        } else {
            window.location.href = '/datacenterlight' + href;
        }
    });
}

/* ---------------------------------------------
 Nav panel classic
 --------------------------------------------- */
if (window.matchMedia("(min-width: 767px)").matches) {
    $('ul.nav li.dropdown').hover(function() {
        $(this).find('.dropdown-menu').stop(true, true).fadeIn(500);
    }, function() {
        $(this).find('.dropdown-menu').stop(true, true).fadeOut(500);
    });
} else {
    /* the viewport is less than 400 pixels wide */
}

$( document ).ready(function() {

	$('[data-toggle="tooltip"]').tooltip();

	var clipboard = new Clipboard('.to_copy');

    clipboard.on('success', function(e) {
        var selector = "#";
        var copy_button_id = selector.concat(e.trigger.id);
        setTimeout(function(){
        	$(copy_button_id).tooltip('hide');
        }, 1000);
    });

    _initNavUrl();

});
// also declared in datacenterlight/js/main.js
function _initNavUrl() {
    // $('.url').click(function(event) {
    //     event.preventDefault();
    //     var href = $(this).attr('href');
    //     $('.navbar-collapse').removeClass('in');
    //     $('.navbar-collapse').addClass('collapsing');
    //     if ($(href).length) {
    //         $('html, body').animate({
    //             scrollTop: $(href).offset().top
    //         }, 1000);
    //     } else {
    //         window.location.href = '/datacenterlight' + href;
    //     }
    // });
    $('.url-init').each(function(idx, el) {
        var $this = $(el);
        var currentPath = window.location.pathname;
        var thisPaths = $this.attr('href').split('#')
        if ($this.hasClass('dropdown-toggle') && window.matchMedia("(max-width: 767px)").matches) {
            $this.removeClass('url-init');
            $this.attr('href', '');
        } else if ($('#'+thisPaths[1]).length) {
            $this.removeClass('url-init').addClass('url');
            $this.attr('href', '#' + thisPaths[1]);
        } else {
            $this.removeClass('url-init');
        }
    });
    $('.url').click(function(event) {
        event.preventDefault();
        var href = $(this).attr('href');
        $('.navbar-collapse').removeClass('in');
        $('.navbar-collapse').addClass('collapsing');
        if ($(href).length) {
            $('html, body').animate({
                scrollTop: $(href).offset().top
            }, 1000);
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

    /*
     * Replace all SVG images with inline SVG
     */
    $('.svg-img').each(function() {
        var $img = $(this);
        var imgID = $img.attr('id');
        var imgClass = $img.attr('class');
        var imgURL = $img.attr('src');

        jQuery.get(imgURL, function(data) {
            // Get the SVG tag, ignore the rest
            var $svg = jQuery(data).find('svg');

            // Add replaced image's ID to the new SVG
            if(typeof imgID !== 'undefined') {
                $svg = $svg.attr('id', imgID);
            }
            // Add replaced image's classes to the new SVG
            if(typeof imgClass !== 'undefined') {
                $svg = $svg.attr('class', imgClass+' replaced-svg');
            }

            // Remove any invalid XML tags as per http://validator.w3.org
            $svg = $svg.removeAttr('xmlns:a');

            // Check if the viewport is set, if the viewport is not set the SVG wont't scale.
            if(!$svg.attr('viewBox') && $svg.attr('height') && $svg.attr('width')) {
                $svg.attr('viewBox', '0 0 ' + $svg.attr('height') + ' ' + $svg.attr('width'))
            }

            // Replace image with new SVG
            $img.replaceWith($svg);

        }, 'xml');
    });

    $('.alt-text').on('mouseenter mouseleave', function(e){
        var $this = $(this);
        var txt = $this.text();
        var alt = $this.attr('data-alt');
        $this.text(alt);
        $this.attr('data-alt', txt);
    });

});

function getScrollbarWidth() {
    var outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.width = "100px";
    outer.style.msOverflowStyle = "scrollbar"; // needed for WinJS apps

    document.body.appendChild(outer);

    var widthNoScroll = outer.offsetWidth;
    // force scrollbars
    outer.style.overflow = "scroll";

    // add innerdiv
    var inner = document.createElement("div");
    inner.style.width = "100%";
    outer.appendChild(inner);

    var widthWithScroll = inner.offsetWidth;

    // remove divs
    outer.parentNode.removeChild(outer);

    return widthNoScroll - widthWithScroll;
}

// globally stores the width of scrollbar
var scrollbarWidth = getScrollbarWidth();
var paddingAdjusted = false;

$( document ).ready(function() {
    // add proper padding to fixed topnav on modal show
    $('body').on('click', '[data-toggle=modal]', function(){
        var $body = $('body');
        if ($body[0].scrollHeight > $body.height()) {
            scrollbarWidth = getScrollbarWidth();
            var topnavPadding = parseInt($('.navbar-fixed-top.topnav').css('padding-right'));
            $('.navbar-fixed-top.topnav').css('padding-right', topnavPadding+scrollbarWidth);
            paddingAdjusted = true;
        }
    });

    // remove added padding on modal hide
    $('body').on('hidden.bs.modal', function(){
        if (paddingAdjusted) {
            var topnavPadding = parseInt($('.navbar-fixed-top.topnav').css('padding-right'));
            $('.navbar-fixed-top.topnav').css('padding-right', topnavPadding-scrollbarWidth);
        }
    });
});
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

    /* ---------------------------------------------
     Scripts initialization
     --------------------------------------------- */
    var cardPricing = {
        'cpu': {
            'id': 'coreValue',
            'value': 1,
            'min': 1,
            'max': 48,
            'interval': 1
        },
        'ram': {
            'id': 'ramValue',
            'value': 2,
            'min': 1,
            'max': 200,
            'interval': 1
        },
        'storage': {
            'id': 'storageValue',
            'value': 10,
            'min': 10,
            'max': 2000,
            'interval': 10
        }
    };

    function _initPricing() {
        _fetchPricing();

        $('.fa-minus-circle.left').click(function(event) {
            var data = $(this).data('minus');

            if (cardPricing[data].value > cardPricing[data].min) {
                cardPricing[data].value = Number(cardPricing[data].value) - cardPricing[data].interval;
            }
            _fetchPricing();
        });
        $('.fa-plus-circle.right').click(function(event) {
            var data = $(this).data('plus');
            if (cardPricing[data].value < cardPricing[data].max) {
                cardPricing[data].value = Number(cardPricing[data].value) + cardPricing[data].interval;
            }
            _fetchPricing();
        });

        $('.input-price').change(function() {
            var data = $(this).attr("name");
            cardPricing[data].value = $('input[name=' + data + ']').val();
            _fetchPricing();
        });
    }

    function _fetchPricing() {
        Object.keys(cardPricing).map(function(element) {
            $('input[name=' + element + ']').val(cardPricing[element].value);
        });
        _calcPricing();
    }

    function _calcPricing() {
        if(typeof window.coresUnitPrice === 'undefined'){
            window.coresUnitPrice = 5;
        }
        if(typeof window.ramUnitPrice === 'undefined'){
            window.ramUnitPrice = 2;
        }
        if(typeof window.ssdUnitPrice === 'undefined'){
            window.ssdUnitPrice = 0.6;
        }
        if(typeof window.discountAmount === 'undefined'){
            window.discountAmount = 0;
        }
        var total = (cardPricing['cpu'].value * window.coresUnitPrice) +
                    (cardPricing['ram'].value * window.ramUnitPrice) +
                    (cardPricing['storage'].value * window.ssdUnitPrice) -
                    window.discountAmount;
        total = parseFloat(total.toFixed(2));
        $("#total").text(total);
    }

    _initPricing();
});
(function($) {
    "use strict"; // Start of use strict


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
            'min': 2,
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
    $(window).load(function() {


    });

    $(document).ready(function() {
        verifiedUrl();
        _navScroll();
        _initScroll();
        _initNavUrl();
        _initPricing();

    });

    $(window).resize(function() {



    });



    /* ---------------------------------------------
     Nav panel classic
     --------------------------------------------- */
    if (window.matchMedia("(min-width: 767px)").matches) {
        $('ul.nav li.dropdown').hover(function() {
            $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeIn(500);
        }, function() {
            $(this).find('.dropdown-menu').stop(true, true).delay(200).fadeOut(500);
        });
    } else {
        /* the viewport is less than 400 pixels wide */
    }



    function _initScroll() {
        $(window).scroll(function() {
            _navScroll();
        });
    }

    function _navScroll() {
        if ($(window).scrollTop() > 10) {
            $(".navbar").removeClass("navbar-transparent");
            $(".navbar-default .btn-link").css("color", "#777");
            $(".dropdown-menu").removeClass("navbar-transparent");
            $(".dropdown-menu > li > a").css("color", "#777");
        } else {
            $(".navbar").addClass("navbar-transparent");
            $(".navbar-default .btn-link").css("color", "#fff");
            $(".dropdown-menu").addClass("navbar-transparent");
            $(".dropdown-menu > li > a").css("color", "#fff");
        }
    }

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

    function verifiedUrl() {
        if (window.location.href.indexOf('#success') > -1) {
            form_success();
        }
    }

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
            //$('#'+cardPricing[element].id).val(cardPricing[element].value);
            $('input[name=' + element + ']').val(cardPricing[element].value);
        });
        _calcPricing();
    }

    function _calcPricing() {
        var total = (cardPricing['cpu'].value * 5) + (2 * cardPricing['ram'].value) + (0.6 * cardPricing['storage'].value);
        total = parseFloat(total.toFixed(2));

        $("#total").text(total);
        $('input[name=total]').val(total);
    }

    function form_success() {
        $('#sucessModal').modal('show');
    }

    function _calculate(numbers, price) {
        $('#valueTotal').text(numbers * price * 31);
    }

})(jQuery);

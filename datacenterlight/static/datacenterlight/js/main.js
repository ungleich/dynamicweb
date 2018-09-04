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
    $(window).load(function() {


    });

    $(document).ready(function() {
        verifiedUrl();
        _navScroll();
        _initScroll();
        _initNavUrl();
        _initPricing();
        ajaxForms();
    });

    $(window).resize(function() {



    });



    /* ---------------------------------------------
     Nav panel classic
     --------------------------------------------- */
    if (window.matchMedia("(min-width: 767px)").matches) {
        $('ul.nav .dropdown').hover(function() {
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

    _navScroll();

    function _initNavUrl() {
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
            var $this = $(this);
            var href = $this.attr('href');
            $('.navbar-collapse').removeClass('in');
            $('.navbar-collapse').addClass('collapsing');
            if (href[0] === "#") {
                scrollToElement(href);
            } else if (href) {
                var path = $(this).prop('href').split('#');
                var currentPath = window.location.origin + window.location.pathname;
                if (currentPath == path[0] && path[1]) {
                    scrollToElement('#' + path[1]);
                } else {
                    window.location = href;
                }
            }
        });
    }

    function scrollToElement(el) {
        var $el = $(el);
        if ($el.length) {
            $('html, body').animate({
                scrollTop: $el.offset().top - 50
            }, 1000);
        }
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

    function form_success() {
        $('#sucessModal').modal('show');
    }

    function _calculate(numbers, price) {
        $('#valueTotal').text(numbers * price * 31);
    }

    function ajaxForms() {
        $('body').on('submit', '.ajax-form', function(e){
            e.preventDefault();
            var $form = $(this);
            $form.find('[type=submit]').addClass('sending');
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: $form.serialize(),

                success: function(response) {
                    var responseContain = $($form.attr('data-response'));
                    responseContain.html(response);
                    $form.find('[type=submit]').removeClass('sending');
                },

                error: function() {
                    $form.find('[type=submit]').removeClass('sending');
                    $form.find('.form-error').removeClass('hide');
                }
            });
        })
    }
})(jQuery);

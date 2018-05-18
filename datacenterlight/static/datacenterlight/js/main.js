(function($) {
    "use strict"; // Start of use strict

    $(document).ready(function() {
        _navScroll();
        _initScroll();
        _initNavUrl();
        ajaxForms();
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

    function ajaxForms() {
        $('body').on('submit', '.ajax-form', function(e){
            e.preventDefault();
            var $form = $(this);
            $form.find('[type=submit]').addClass('sending');
            $.ajax({
                url: $form.attr('action'),
                type: $form.attr('method'),
                data: $form.serialize()
            }).done(function(response) {
                    var responseContain = $($form.attr('data-response'));
                    responseContain.html(response);
            }).error(function() {
                    $form.find('.form-error').removeClass('hide');
            }).always(function() {
                    $form.find('[type=submit]').removeClass('sending');
            });
        })
    }
})(jQuery);

(function($){
    'use strict'; // Start of use strict

   

    $(document).ready(function(){
        verifiedUrl();
        init_options_interested();
        init_nav();
        change_values();
    });

    function verifiedUrl(){
        if(window.location.href.indexOf('#success') > -1){
            form_success();
        }
    }

    function init_options_interested(){
        $('.row-vms').click(function(){
            $('.row-vms').removeClass('row-vms__active');
            $(this).addClass('row-vms__active');
            var number = $('.row-vms__active input').val();
            var price = $('.row-vms__active input').data('price');
            _calculate(number, price);
        });
    }

    function init_nav(){

        $('.nav-local').click(function(){
            $('html, body').animate({
                 scrollTop: $('#'+$(this).data('href')).offset().top
             });
        });
        
    }

    function change_values(){
        $('.number-vms').keyup(function () {
            var number = $(this).val();
            var price =  $(this).data('price');
            _calculate(number, price);
        });

    }
    function form_success(){
        $('#sucessModal').modal('show');
    }
    function _calculate(numbers, price){
        $('#valueTotal').text(numbers*price*31);
    }
    
    
})(jQuery); // End of use strict

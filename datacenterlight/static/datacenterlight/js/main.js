(function($){
    "use strict"; // Start of use strict
    
    
    /* ---------------------------------------------
     Scripts initialization
     --------------------------------------------- */
    var cardPricing ={
        'cpu': {
            'id': 'coreValue',
            'value': 1,
            'min':1,
            'max': 48,
            'interval': 1
        },
        'ram': {
            'id': 'ramValue',
            'value': 2,
            'min':2,
            'max': 200,
            'interval': 1
        },
        'storage': {
            'id': 'storageValue',
            'value': 10,
            'min': 10,
            'max': 500,
            'interval': 10
        }
    }
    $(window).load(function(){
    
  
    });
    
    $(document).ready(function(){
        verifiedUrl();
       _navScroll();
       _initScroll();
       _initNavUrl();
       _initPricing();
       
    });
    
    $(window).resize(function(){
        
        
        
    });
    


    /* ---------------------------------------------
     Nav panel classic
     --------------------------------------------- */
    
    
    function _initScroll(){
        $(window).scroll(function(){     
          _navScroll();
        });

    }

    function _navScroll(){
       	if($(window).scrollTop() > 10 ){
            $(".navbar").removeClass("navbar-transparent");
            $(".navbar-default .btn-link").css("color", "#777");
        }else{
            $(".navbar").addClass("navbar-transparent");
            $(".navbar-default .btn-link").css("color", "#fff");
        }
    }
	function _initNavUrl(){
        $('.url').click(function(){
             var href = $(this).attr('data-url');
             $('.navbar-collapse').removeClass('in');
             $('.navbar-collapse').addClass('collapsing');
             $('html, body').animate({
                scrollTop: $(href).offset().top
            }, 1000);
        });
    }
    function verifiedUrl(){
        if(window.location.href.indexOf('#success') > -1){
            form_success();
            console.log('epa');
        }
    }

    function _initPricing(){
        _fetchPricing();

        $('.fa-minus-circle.left').click(function(event){
            var data = $(this).data('minus');
            
            if(cardPricing[data].value > cardPricing[data].min){
                cardPricing[data].value = Number(cardPricing[data].value) - cardPricing[data].interval;
            }
            _fetchPricing();
        });
        $('.fa-plus-circle.right').click(function(event){
            var data = $(this).data('plus');
            if(cardPricing[data].value < cardPricing[data].max){
                cardPricing[data].value = Number(cardPricing[data].value) + cardPricing[data].interval;
            }
            _fetchPricing();
        });

        $('.input-price').change(function(){
            var data = $(this).attr("name");
            cardPricing[data].value = $('input[name='+data+']').val();
            _fetchPricing();
        });
    }
    function _fetchPricing(){
        Object.keys(cardPricing).map(function(element){
            //$('#'+cardPricing[element].id).val(cardPricing[element].value);
            $('input[name='+element+']').val(cardPricing[element].value);
        });
        _calcPricing();
    }

    function _calcPricing(){
        var total = (cardPricing['cpu'].value * 5) + (2* cardPricing['ram'].value) + (0.6* cardPricing['storage'].value); 
        total = parseFloat(total.toFixed(2));

        $("#total").text(total);
        $('input[name=total]').val(total);
    }
    function form_success(){
        $('#sucessModal').modal('show');
    }
    function _calculate(numbers, price){
        $('#valueTotal').text(numbers*price*31);
    }
    
  
    
})(jQuery); 
// (function($){
//     'use strict'; // Start of use strict

   

//     $(document).ready(function(){
//         verifiedUrl();
//         init_options_interested();
//         init_nav();
//         change_values();
//     });

//     function verifiedUrl(){
//         if(window.location.href.indexOf('#success') > -1){
//             form_success();
//         }
//     }

//     function init_options_interested(){
//         $('.row-vms').click(function(){
//             $('.row-vms').removeClass('row-vms__active');
//             $(this).addClass('row-vms__active');
//             var number = $('.row-vms__active input').val();
//             var price = $('.row-vms__active input').data('price');
//             _calculate(number, price);
//         });
//     }

//     function init_nav(){

//         $('.nav-local').click(function(){
//             $('html, body').animate({
//                  scrollTop: $('#'+$(this).data('href')).offset().top
//              });
//         });
        
//     }

//     function change_values(){
//         $('.number-vms').keyup(function () {
//             var number = $(this).val();
//             var price =  $(this).data('price');
//             _calculate(number, price);
//         });

//     }
//     function form_success(){
//         $('#sucessModal').modal('show');
//     }
//     function _calculate(numbers, price){
//         $('#valueTotal').text(numbers*price*31);
//     }
    
    
// })(jQuery); // End of use strict


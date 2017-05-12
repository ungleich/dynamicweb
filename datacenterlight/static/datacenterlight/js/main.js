
(function($){
    "use strict"; // Start of use strict
    
    
    /* ---------------------------------------------
     Scripts initialization
     --------------------------------------------- */
    
    $(window).load(function(){
    
  
    });
    
    $(document).ready(function(){
        
       _navScroll();
       _initScroll();
       _initNavUrl();
       
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
       		console.log($(window).scrollTop());
            $(".navbar").removeClass("navbar-transparent");
        }else{
            $(".navbar").addClass("navbar-transparent");
        }
    }
	function _initNavUrl(){
        $('.url').click(function(){
             var href = $(this).attr('data-url');
             console.log(href);
             $('html, body').animate({
                scrollTop: $(href).offset().top
            }, 1000);
        });
    }
    
  
    
})(jQuery); // End of use strict
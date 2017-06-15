(function($){
    "use strict"; // Start of use strict
    
    
    $(window).load(function(){
    
  
    });
    
    $(document).ready(function(){
      _initOs();
       
    });
    
    $(window).resize(function(){
        
        
    });
    


   	function _initOs(){

   		
   		$('.os-circle').click(function(event){
   			$('.os-circle').removeClass('active');
   			$(this).addClass('active');

        var idTemplate = $(this).data('id');
        $('input[name=vm_template_id]').val(idTemplate);
   		});
   		$('.config-box').click(function(event){
   			$('.config-box').removeClass('active');
   			$(this).addClass('active');
        var idConfig = $(this).data('id');
        var price = $(this).data('price');
        $('input[name=configuration]').val(idConfig);
        $('.container-button').fadeIn();
        $('#priceValue').text(price);
   		});

		$('.owl-carousel').owlCarousel({
        items:4,
        nav: true,
        margin:30,
        responsiveClass:true,
        navText: ['<i class="fa fa-angle-left"></i>', '<i class="fa fa-angle-right"></i>'],
        responsive:{
            0:{
                items:1,
                nav:true
            },
            600:{
                items:2,
                nav:true
            },
            768:{
                items:3,
                nav:true
            },
            990:{
                items:4,
                nav:true
            }
        }
		});
	}
    
    
    
})(jQuery); 



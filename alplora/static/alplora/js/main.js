(function($){
	'use strict';

	$(window).load(function(){

	// Page loader

		$("body").imagesLoaded(function(){
		    $(".page-loader div").fadeOut();
		    $(".page-loader").delay(200).fadeOut("slow");
		});

	});


	$( document ).ready(function() {
		init_nav();
		initBackgroundsHeader();
		init_hovers();
	});
	
	//Infinite loop for change Background Header
	function _changeBg(index, arrayEl, time){
		if(index===0)
			$(arrayEl[0]).fadeIn(2000);
		setTimeout(function(){
            $(arrayEl[index]).fadeOut(2000);
            if(index+1 < arrayEl.length)
            	$(arrayEl[index+1]).fadeIn(2000);

           return index+1 === arrayEl.length ? _changeBg(0, arrayEl, time): _changeBg(index+1, arrayEl, time);
        }, time);
	}
	function initBackgroundsHeader(){
		var arrayElements = [];
		for(var index=0; index<$('.intro-header .bg-slide').length; index++ ){
			arrayElements.push($('.intro-header .bg-slide')[index]);
		}
		_changeBg(0, arrayElements, 4000);
	}

	function init_nav(){

    	$('.nav-local').click(function(){
			$('html, body').animate({
                 scrollTop: $('#'+$(this).data('href')).offset().top
             });
    	});
    	
    }

    function init_hovers(){
    	$('.select-language').hover(function() {
		    $('.drop-language').show();
		  }, function() {
		    $('.drop-language').hide();
		})
    	$('.drop-language').hover(function() {
		    $('.drop-language').show();
		  }, function() {
		    $('.drop-language').hide();
		})
    }

})(jQuery);
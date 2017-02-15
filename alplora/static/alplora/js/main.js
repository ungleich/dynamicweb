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

		initBackgroundsHeader();
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
		var arrayElements = Array.from($('.intro-header .bg-slide'));
		_changeBg(0, arrayElements, 4000);
	}

})(jQuery);
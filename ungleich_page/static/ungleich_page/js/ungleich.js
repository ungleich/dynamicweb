/* globals $, WOW */

$(function(){
    new WOW().init();
    $('.img-toggle').one('mouseover', toggleImage);
});

function toggleImage(e) {
    var $this = $(this),
	toggle_img = $this.attr('data-replaced'),
	current_img = $this.attr('src');
    $this.fadeOut(600, function() {
	$this.attr('src', toggle_img);
	$this.attr('data-replaced', current_img);
	$this.fadeIn(900);
    });
};

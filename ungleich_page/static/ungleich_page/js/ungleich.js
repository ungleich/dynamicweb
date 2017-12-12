/* globals $, WOW */

$(function(){
    new WOW().init();
    $('.img-toggle').one('mouseenter', toggleImage);
});

function toggleImage(e) {
    var $this = $(this),
	toggle_img = $this.attr('data-replaced'),
	current_img = $this.attr('src');
    $this.fadeOut(200, function() {
	$this.attr('src', toggle_img);
	$this.attr('data-replaced', current_img);
	$this.fadeIn(300);
    });
};

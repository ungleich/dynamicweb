$( document ).ready(function() {


	$('[data-toggle="tooltip"]').tooltip();

	var clipboard = new Clipboard('.to_copy');

    clipboard.on('success', function(e) {
        var selector = "#";
        var copy_button_id = selector.concat(e.trigger.id);
        setTimeout(function(){
        	$(copy_button_id).tooltip('hide');
        }, 1000);
    });

    $('.alt-text').on('mouseenter mouseleave', function(e){
        var $this = $(this);
        var txt = $this.text();
        var alt = $this.attr('data-alt');
        $this.text(alt);
        $this.attr('data-alt', txt);
    });

});
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

});
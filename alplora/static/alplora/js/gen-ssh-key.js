$( document ).ready(function() {





	// Create a file with ssh private key info 
	function donwloadKeyFile(){

		var key = $('#ssh_key').text();
		var a = window.document.createElement('a');

		a.href = window.URL.createObjectURL(new Blob([key], {type: 'text'}));
		a.download = 'private_key.pem';

		// Append anchor to body.
		document.body.appendChild(a);
		a.click();

		// Remove anchor from body
		document.body.removeChild(a);

	}


	// Create a file with ssh private key info 
	$('#download_ssh_key').on('click',donwloadKeyFile);	


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

$( document ).ready(function() {

	$('#confirm-cancel').on('click', '.btn-ok', function(e) {
		$('#virtual_machine_cancel_form').trigger('submit');
	});

  var hash = window.location.hash;
  hash && $('ul.nav a[href="' + hash + '"]').tab('show');

  $('.nav-tabs a').click(function (e) {
    $(this).tab('show');
    var scrollmem = $('body').scrollTop() || $('html').scrollTop();
    window.location.hash = this.hash;
    $('html,body').scrollTop(scrollmem);
  });

});
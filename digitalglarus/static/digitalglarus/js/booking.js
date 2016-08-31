$( document ).ready(function() {

	// $('#booking-date-range').daterangepicker();


	$('#booking-date-range').daterangepicker({
		autoUpdateInput: false,
		locale: {
		  cancelLabel: 'Clear'
		}
	});


	$('#booking-date-range').on('apply.daterangepicker', function(ev, picker) {
		$(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
	});

	$('#booking-date-range').on('cancel.daterangepicker', function(ev, picker) {
		$(this).val('Select your dates');
	});

});
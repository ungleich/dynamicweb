$( document ).ready(function() {


	// $('#booking-date-range').daterangepicker();

	var tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
	// var tomorrow = today.setDate(today.getDate() + 1);
	$('#booking-date-range').daterangepicker({
		autoUpdateInput: false,
		locale: {
		  cancelLabel: 'Clear'
		},
		minDate: tomorrow,
	});


	$('#booking-date-range').on('apply.daterangepicker', function(ev, picker) {
		$(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
	});

	$('#booking-date-range').on('cancel.daterangepicker', function(ev, picker) {
		$(this).val('Select your dates');
	});

});
$( document ).ready(function() {


	// $('#booking-date-range').daterangepicker();




		var tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
        $('#booking-date-1').datetimepicker({
        	// minDate: tomorrow,
        	format: 'MM/d/YYYY',
        	defaultDate: false
        });
        $('#booking-date-2').datetimepicker({
            useCurrent: false, //Important! See issue #1075
            format: 'MM/d/YYYY',
        });
        $("#booking-date-1").on("dp.change", function (e) {
            $('#booking-date-2').data("DateTimePicker").minDate(e.date);
        });
        $("#booking-date-2").on("dp.change", function (e) {
            $('#booking-date-1').data("DateTimePicker").maxDate(e.date);
        });


	// var tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);
	// // var tomorrow = today.setDate(today.getDate() + 1);
	// $('#booking-date-range').daterangepicker({
	// 	autoUpdateInput: false,
	// 	locale: {
	// 	  cancelLabel: 'Clear'
	// 	},
	// 	minDate: tomorrow,
	// });


	// $('#booking-date-range').on('apply.daterangepicker', function(ev, picker) {
	// 	$(this).val(picker.startDate.format('MM/DD/YYYY') + ' - ' + picker.endDate.format('MM/DD/YYYY'));
	// });

	// $('#booking-date-range').on('dp.cancel', function(ev, picker) {
	// 	$(this).val('Select your dates');
	// });

});
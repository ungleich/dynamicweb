$( document ).ready(function() {


	// $('#booking-date-range').daterangepicker();




		var tomorrow = new Date(new Date().getTime() + 24 * 60 * 60 * 1000);

        $('#booking-date-1').datetimepicker({
        	minDate: tomorrow,
        	format: 'MM/DD/YYYY',
        	// defaultDate: false
        });
        $('#booking-date-1').val('');
        $('#booking-date-2').datetimepicker({
            useCurrent: false, //Important! See issue #1075
            format: 'MM/DD/YYYY',
        });
        $("#booking-date-1").on("dp.change", function (e) {
            $('#booking-date-2').data("DateTimePicker").minDate(e.date);
        });
        $("#booking-date-2").on("dp.change", function (e) {
            $('#booking-date-1').data("DateTimePicker").maxDate(e.date);
        });

});
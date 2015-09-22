function day_diff(d1, d2) {
    var one_day=1000*60*60*24;
    var date1_ms = d1.getTime();
    var date2_ms = d2.getTime();
    var difference_ms = date2_ms - date1_ms;
    return Math.round(difference_ms/one_day);
}

$(function(){
    //  $progressbar = $("#progressbar"),
    //	$progressbarLabel = $("progressbar-label"),
    //	$progrssbarLabelDays = $("progrssbar-label-days"),
    var date_start = new Date(2015, 8, 22),
	date_end = new Date(2015, 11, 31),
	current_date = new Date(),
	total_days = 100,
	days_pass = day_diff(date_start, current_date),
	$date  = $("#date-quantity"),
	days_to_go = total_days - days_pass;
    $date.html(days_to_go.toString());
});

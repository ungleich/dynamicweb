$(document).ready(function() {
    $('.btn-pdf').click(function(e) {
        e.preventDefault();
        var $target = $($(this).attr('data-target')) || $('body');
        var fileName = $target.attr('id') + '.pdf';
        html2pdf($target[0], {
            filename: fileName,
        });
    });
    $('.btn-print').click(function(e) {
        e.preventDefault();
        console.log('a');
        window.print();
    });
});
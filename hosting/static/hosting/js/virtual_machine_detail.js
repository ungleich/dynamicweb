$(document).ready(function() {

    $('#confirm-cancel').on('click', '.btn-ok', function(e) {
        var url = $('#virtual_machine_cancel_form').attr('action');
        var $container = $('#terminate-VM');
        var $btn = $container.find('.btn');
        var text = $container.find('.vm-item-lg').text();
        var altText = $container.attr('data-alt');
        $container.find('.alert-danger').addClass('hide');
        $container.addClass('processing')
            .find('.vm-item-lg').attr('class', '')
            .addClass('vm-item-lg vm-color-failed')
            .text(altText);
        $btn.prop('disabled', true);
        $('#confirm-cancel').modal('hide');
        $.post(url)
            .done(function(data) {
                console.log("success", data);
                if (data.status == true) {
                    $container.addClass('terminate-success')
                        .find('.vm-item-lg').text(data.text);
                    $btn.remove();
                    window.location = data.redirect;
                } else {
                    $container.addClass('terminate-fail')
                        .find('.vm-item-lg').text(text);
                    $container.find('.btn').prop('disabled', false);
                    $container.find('.alert-danger').text(data.text).removeClass('hide');
                }
            })
            .fail(function(data) {
                $container.addClass('terminate-fail')
                    .find('.vm-item-lg').text(text);
                $container.find('.btn').prop('disabled', false);
                $container.find('.alert-danger').removeClass('hide');
            })
            .always(function(data) {
                $container.removeClass('processing');
            });
    });

    var hash = window.location.hash;
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    $('.nav-tabs a').click(function(e) {
        $(this).tab('show');
        var scrollmem = $('body').scrollTop() || $('html').scrollTop();
        window.location.hash = this.hash;
        $('html,body').scrollTop(scrollmem);
    });

});
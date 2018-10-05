$( document ).ready(function() {
    var clipboard = new Clipboard('.to_copy');

    clipboard.on('success', function(e) {
        var selector = "#";
        var copy_button_id = selector.concat(e.trigger.id);
        setTimeout(function(){
            $(copy_button_id).tooltip('hide');
        }, 1000);
    });
});

function VMTerminateStatus($container, url) {
    $.ajax({
        url: url,
        type: 'GET',
        dataType: 'json',
        success: function(data) {
            VMTerminateSuccess($container, data);
        },
        error: function() {
            setTimeout(function(){
                VMTerminateStatus($container, url);
            }, 5000);
        }
    });
}

function VMTerminateActive($container, altText) {
    $container.find('.alert-danger').addClass('hide');
    $container.addClass('processing')
        .find('.vm-item-lg').attr('class', '')
        .addClass('vm-item-lg vm-color-failed')
        .text(altText);
    $container.find('.btn').prop('disabled', true);
    $('#confirm-cancel').modal('hide');
}

function VMTerminateSuccess($container, data) {
    $container.addClass('terminate-success')
        .find('.vm-item-lg').text(data.text);
    $container.find('.btn').remove();
    $('#terminate-success').modal('show');
}

function VMTerminateFail($container, data, text) {
    $container.addClass('terminate-fail')
        .find('.vm-item-lg').text(text);
    $container.find('.btn').prop('disabled', false);
    $container.find('.alert-danger').text(data.text).removeClass('hide');
    $container.removeClass('processing');
}


$(document).ready(function() {
    $('#confirm-cancel').on('click', '.btn-ok', function(e) {
        var url = $('#virtual_machine_cancel_form').attr('action');
        var $container = $('#terminate-VM');
        var text = $container.find('.vm-item-lg').text();
        var altText = $container.attr('data-alt');
        VMTerminateActive($container, altText);

        $.post(url)
            .done(function(data) {
                if (data.status == true) {
                    VMTerminateSuccess($container, data);
                } else {
                    if ('text' in data) {
                        VMTerminateFail($container, data, text);
                    } else {
                        VMTerminateStatus($container, url);
                    }
                }
            })
            .fail(function(data) {
                if (data.status==504) {
                    VMTerminateStatus($container, url);
                } else {
                    VMTerminateFail($container, data, text);
                }
            })
    });

    var hash = window.location.hash;
    hash && $('ul.nav a[href="' + hash + '"]').tab('show');

    $('.nav-tabs a').click(function(e) {
        $(this).tab('show');
        var scrollmem = $('body').scrollTop() || $('html').scrollTop();
        window.location.hash = this.hash;
        $('html,body').scrollTop(scrollmem);
    });

    var create_vm_form = $('#virtual_machine_create_form');
    create_vm_form.submit(function () {
        $('#btn-create-vm').prop('disabled', true);
        $.ajax({
            url: create_vm_form.attr('action'),
            type: 'POST',
            data: create_vm_form.serialize(),
            init: function(){
                ok_btn = $('#createvm-modal-done-btn');
                close_btn = $('#createvm-modal-close-btn');
                ok_btn.addClass('btn btn-success btn-ok btn-wide hide');
                close_btn.addClass('btn btn-danger btn-ok btn-wide hide');
            },
            success: function (data) {
                fa_icon = $('.modal-icon > .fa');
                modal_btn = $('#createvm-modal-done-btn');
                $('#createvm-modal-title').text(data.msg_title);
                $('#createvm-modal-body').html(data.msg_body);
                modal_btn.attr('href', data.redirect)
                    .removeClass('hide');
                if (data.status === true) {
                    fa_icon.attr('class', 'checkmark');
                } else {
                    fa_icon.attr('class', 'fa fa-close');
                    modal_btn.attr('class', '').addClass('btn btn-danger btn-ok btn-wide');
                }
            },
            error: function (xmlhttprequest, textstatus, message) {
                    fa_icon = $('.modal-icon > .fa');
                    fa_icon.attr('class', 'fa fa-close');
                    if (typeof(create_vm_error_message) !== 'undefined') {
                        $('#createvm-modal-body').text(create_vm_error_message);
                    }
                    $('#btn-create-vm').prop('disabled', false);
                    $('#createvm-modal-close-btn').removeClass('hide');
            }
        });
        return false;
    });
    $('#createvm-modal').on('hidden.bs.modal', function () {
        $(this).find('.modal-footer .btn').addClass('hide');
    })
});

window.onload = function () {
    var locale_dates = document.getElementsByClassName("locale_date");
    var formats = ['YYYY-MM-DD hh:mm a'];
    var i;
    for (i = 0; i < locale_dates.length; i++) {
        var oldDate = moment.utc(locale_dates[i].textContent, formats);
        var outputFormat = locale_dates[i].getAttribute('data-format') || oldDate._f;
        locale_dates[i].innerHTML = oldDate.local().format(outputFormat);
        locale_dates[i].className += ' done';
    }
};
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
            success: function (data) {
                if (data.status === true) {
                    fa_icon = $('.modal-icon > .fa');
                    fa_icon.attr('class', 'fa fa-check');
                    $('.modal-header > .close').attr('class', 'close');
                    $('#createvm-modal-title').text(data.msg_title);
                    $('#createvm-modal-body').text(data.msg_body);
                    $('#createvm-modal').on('hidden.bs.modal', function () {
                        window.location = data.redirect;
                    })
                }
            },
            error: function (xmlhttprequest, textstatus, message) {
                    fa_icon = $('.modal-icon > .fa');
                    fa_icon.attr('class', 'fa fa-times');
                    $('.modal-header > .close').attr('class', 'close');
                    if (typeof(create_vm_error_message) !== 'undefined') {
                        $('#createvm-modal-title').text(create_vm_error_message);
                    }
                    $('#btn-create-vm').prop('disabled', false);
            }
        });
        return false;
    });
});

$( document ).ready(function() {


	$('[data-toggle="tooltip"]').tooltip();

	var clipboard = new Clipboard('.to_copy');

    clipboard.on('success', function(e) {
        var selector = "#";
        var copy_button_id = selector.concat(e.trigger.id);
        setTimeout(function(){
        	$(copy_button_id).tooltip('hide');
        }, 1000);
    });

});

function getScrollbarWidth() {
    var outer = document.createElement("div");
    outer.style.visibility = "hidden";
    outer.style.width = "100px";
    outer.style.msOverflowStyle = "scrollbar"; // needed for WinJS apps

    document.body.appendChild(outer);

    var widthNoScroll = outer.offsetWidth;
    // force scrollbars
    outer.style.overflow = "scroll";

    // add innerdiv
    var inner = document.createElement("div");
    inner.style.width = "100%";
    outer.appendChild(inner);

    var widthWithScroll = inner.offsetWidth;

    // remove divs
    outer.parentNode.removeChild(outer);

    return widthNoScroll - widthWithScroll;
}

// globally stores the width of scrollbar
var scrollbarWidth = getScrollbarWidth();

// add proper padding to fixed topnav on modal show
$('body').on('click', '[data-toggle=modal]', function(){
    var topnavPadding = parseInt($('.navbar-fixed-top.topnav').css('padding-right'));
    $('.navbar-fixed-top.topnav').css('padding-right', topnavPadding+scrollbarWidth);
});

// remove added padding on modal hide
$('body').on('hidden.bs.modal', function(){
    var topnavPadding = parseInt($('.navbar-fixed-top.topnav').css('padding-right'));
    $('.navbar-fixed-top.topnav').css('padding-right', topnavPadding-scrollbarWidth);
});
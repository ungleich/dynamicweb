(function($){
    "use strict"; // Start of use strict

    var cardPricing = {
        'cpu': {
            'id': 'coreValue',
            'value': 1,
            'min': 1,
            'max': 48,
            'interval': 1
        },
        'ram': {
            'id': 'ramValue',
            'value': 1,
            'min': 1,
            'max': 200,
            'interval': 1
        },
        'storage': {
            'id': 'storageValue',
            'value': 10,
            'min': 10,
            'max': 2000,
            'interval': 10
        }
    };

    function _initPricing() {
        _fetchPricing();

        $('.fa-minus.left').click(function(event) {
            var data = $(this).data('minus');

            if (cardPricing[data].value > cardPricing[data].min) {
                cardPricing[data].value = Number(cardPricing[data].value) - cardPricing[data].interval;
            }
            _fetchPricing();
        });
        $('.fa-plus.right').click(function(event) {
            var data = $(this).data('plus');
            if (cardPricing[data].value < cardPricing[data].max) {
                cardPricing[data].value = Number(cardPricing[data].value) + cardPricing[data].interval;
            }
            _fetchPricing();
        });

        $('.input-price').change(function() {
            var data = $(this).attr("name");
            cardPricing[data].value = $('input[name=' + data + ']').val();
            _fetchPricing();
        });
    }

    function _fetchPricing() {
        Object.keys(cardPricing).map(function(element) {
            $('input[name=' + element + ']').val(cardPricing[element].value);
        });
        _calcPricing();
    }

    function _calcPricing() {
        var total = (cardPricing['cpu'].value * 5) + (2 * cardPricing['ram'].value) + (0.6 * cardPricing['storage'].value);
        total = parseFloat(total.toFixed(2));

        $("#total").text(total);
        $('input[name=total]').val(total);
    }

    $(document).ready(function() {
        _initPricing();
    });

})(jQuery);



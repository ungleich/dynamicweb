(function($) {
    "use strict"; // Start of use strict
    var calculatorParams = {};

    $(document).ready(function() {
        _initPricing();
    });

    function stepInput(fa, action) {
        var $fa = $(fa);
        var name = $fa.data(action);
        var $input = $fa.closest('form').find('input[name="'+name+'"]');
        var val = Number($input.val());
        var step = Number($input.prop('step')) || 1;
        var newVal = val;
        if (action === 'minus') {
            newVal -= step;
        } else if (action === 'plus') {
            newVal += step;
        }
        if (newVal <= Number($input.prop('max')) && newVal >= Number($input.prop('min'))) {
            $input.val(newVal).trigger('change');
        }
    }

    $('[data-minus]').click(function() {
        stepInput(this, 'minus');
    });

    $('[data-plus]').click(function() {
        stepInput(this, 'plus');
    });

    $('.input-price').change(function() {
        var $this = $(this);
        var name = $this.attr('name');
        console.log(name)
        var formId = $this.closest('.calculator_container').attr('id');
        calculatorParams[formId][name].value = Number($this.val());
        _calculateTotal(formId);
    });

    function _initPricing() {
        $('.calculator_container').each(function(idx, el) {
            var $el = $(el);
            var id = $el.attr('id');
            calculatorParams[id] = {};
            $el.find('.input-price').each(function() {
                var $this = $(this);
                console.log($this.val())
                var name = $this.prop('name');
                calculatorParams[id][name] = {
                    'min': Number($this.prop('min')),
                    'max': Number($this.prop('max')),
                    'step': Number($this.prop('step')) || 1,
                    'price': Number($this.data('price')) || 1,
                    'value': Number($this.val())
                };
            });
            console.log(calculatorParams)
            _calculateTotal(id);
        });
    }

    function _calculateTotal(formId) {
        var cardPricing = calculatorParams[formId];
        var total = 0;
        Object.keys(cardPricing).map(function(name) {
            total += cardPricing[name].price * cardPricing[name].value;
        });
        $('#'+formId).find(".total").text(total);
    }
})(jQuery);
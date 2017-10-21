var cardBrandToPfClass = {
    'visa': 'pf-visa',
    'mastercard': 'pf-mastercard',
    'amex': 'pf-american-express',
    'discover': 'pf-discover',
    'diners': 'pf-diners',
    'jcb': 'pf-jcb',
    'unknown': 'pf-credit-card'
};
function setBrandIcon(brand) {
    var brandIconElement = document.getElementById('brand-icon');
    var pfClass = 'pf-credit-card';
    if (brand in cardBrandToPfClass) {
        pfClass = cardBrandToPfClass[brand];
    }
    for (var i = brandIconElement.classList.length - 1; i >= 0; i--) {
        brandIconElement.classList.remove(brandIconElement.classList[i]);
    }
    brandIconElement.classList.add('pf');
    brandIconElement.classList.add(pfClass);
}


$(document).ready(function () {
    $.ajaxSetup({
        beforeSend: function (xhr, settings) {
            function getCookie(name) {
                var cookieValue = null;
                if (document.cookie && document.cookie != '') {
                    var cookies = document.cookie.split(';');
                    for (var i = 0; i < cookies.length; i++) {
                        var cookie = jQuery.trim(cookies[i]);
                        // Does this cookie string begin with the name we want?
                        if (cookie.substring(0, name.length + 1) == (name + '=')) {
                            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                            break;
                        }
                    }
                }
                return cookieValue;
            }

            if (!(/^http:.*/.test(settings.url) || /^https:.*/.test(settings.url))) {
                // Only send the token to relative URLs i.e. locally.
                xhr.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
            }
        }
    });


    var hasCreditcard = window.hasCreditcard || false;
    if (!hasCreditcard && window.stripeKey) {
        var stripe = Stripe(window.stripeKey);
        var element_style = {
            fonts: [{
                family: 'lato-light',
                src: 'url(https://cdn.jsdelivr.net/font-lato/2.0/Lato/Lato-Light.woff) format("woff2")'
            }, {
                family: 'lato-regular',
                src: 'url(https://cdn.jsdelivr.net/font-lato/2.0/Lato/Lato-Regular.woff) format("woff2")'
            }
            ],
            locale: window.current_lan
        };
        var elements = stripe.elements(element_style);
        var credit_card_text_style = {
            base: {
                iconColor: '#666EE8',
                color: '#31325F',
                lineHeight: '25px',
                fontWeight: 300,
                fontFamily: "'lato-light', sans-serif",
                fontSize: '14px',
                '::placeholder': {
                    color: '#777'
                }
            },
            invalid: {
                iconColor: '#eb4d5c',
                color: '#eb4d5c',
                lineHeight: '25px',
                fontWeight: 300,
                fontFamily: "'lato-regular', sans-serif",
                fontSize: '14px',
                '::placeholder': {
                    color: '#eb4d5c',
                    fontWeight: 400
                }
            }
        };

        var enter_ccard_text = "Enter your credit card number";
        if (typeof window.enter_your_card_text !== 'undefined') {
            enter_ccard_text = window.enter_your_card_text;
        }
        var cardNumberElement = elements.create('cardNumber', {
            style: credit_card_text_style,
            placeholder: enter_ccard_text
        });
        cardNumberElement.mount('#card-number-element');

        var cardExpiryElement = elements.create('cardExpiry', {
            style: credit_card_text_style
        });
        cardExpiryElement.mount('#card-expiry-element');

        var cardCvcElement = elements.create('cardCvc', {
            style: credit_card_text_style
        });
        cardCvcElement.mount('#card-cvc-element');
        cardNumberElement.on('change', function (event) {
            if (event.brand) {
                setBrandIcon(event.brand);
            }
        });
    }

    var submit_form_btn = $('#payment_button_with_creditcard');
    submit_form_btn.on('click', submit_payment);


    function submit_payment(e) {
        e.preventDefault();
        $('#billing-form').submit();
    }


    var $form_new = $('#payment-form-new');
    $form_new.submit(payWithStripe_new);

    function payWithStripe_new(e) {
        e.preventDefault();

        function stripeTokenHandler(token) {
            // Insert the token ID into the form so it gets submitted to the server
            $('#id_token').val(token.id);
            $('#billing-form').submit();
        }


        stripe.createToken(cardNumberElement).then(function (result) {
            if (result.error) {
                // Inform the user if there was an error
                var errorElement = document.getElementById('card-errors');
                errorElement.textContent = result.error.message;
            } else {
                var process_text = "Processing";
                if (typeof window.processing_text !== 'undefined') {
                    process_text = window.processing_text
                }

                $form_new.find('[type=submit]').html(process_text + ' <i class="fa fa-spinner fa-pulse"></i>');
                // Send the token to your server
                stripeTokenHandler(result.token);
            }
        });
    }

    /* Form validation */
    $.validator.addMethod("month", function (value, element) {
        return this.optional(element) || /^(01|02|03|04|05|06|07|08|09|10|11|12)$/.test(value);
    }, "Please specify a valid 2-digit month.");

    $.validator.addMethod("year", function (value, element) {
        return this.optional(element) || /^[0-9]{2}$/.test(value);
    }, "Please specify a valid 2-digit year.");

    validator = $form_new.validate({
        rules: {
            cardNumber: {
                required: true,
                creditcard: true,
                digits: true
            },
            expMonth: {
                required: true,
                month: true
            },
            expYear: {
                required: true,
                year: true
            },
            cvCode: {
                required: true,
                digits: true
            }
        },
        highlight: function (element) {
            $(element).closest('.form-control').removeClass('success').addClass('error');
        },
        unhighlight: function (element) {
            $(element).closest('.form-control').removeClass('error').addClass('success');
        },
        errorPlacement: function (error, element) {
            $(element).closest('.form-group').append(error);
        }
    });

    $('.credit-card-info .btn.choice-btn').click(function(){
            var id = this.dataset['id_card'];
            $('#id_card').val(id);
            $('#billing-form').submit();
    });
});


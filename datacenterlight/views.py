import logging

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse, Http404
from django.shortcuts import render
from django.utils.translation import get_language, ugettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, CreateView, DetailView

from hosting.forms import (
    HostingUserLoginForm, GenericPaymentForm, ProductPaymentForm
)
from hosting.models import (
    HostingBill, HostingOrder, UserCardDetail, GenericProduct
)
from membership.models import CustomUser, StripeCustomer
from opennebula_api.serializers import VMTemplateSerializer
from utils.forms import (
    BillingAddressForm, BillingAddressFormSignup, UserBillingAddressForm,
    BillingAddress
)
from utils.hosting_utils import get_vm_price_with_vat
from utils.stripe_utils import StripeUtils
from utils.tasks import send_plain_email_task
from .forms import ContactForm
from .models import VMTemplate, VMPricing
from .utils import get_cms_integration, create_vm

logger = logging.getLogger(__name__)


class ContactUsView(FormView):
    template_name = "datacenterlight/contact_form.html"
    form_class = ContactForm

    def get(self, request, *args, **kwargs):
        return HttpResponseRedirect(reverse('datacenterlight:index'))

    def form_invalid(self, form):
        if self.request.is_ajax():
            return self.render_to_response(
                self.get_context_data(contact_form=form))
        else:
            return render(
                self.request, 'datacenterlight/index.html',
                self.get_context_data(contact_form=form)
            )

    def form_valid(self, form):
        form.save()
        from_emails = {
            'glasfaser': 'glasfaser@ungleich.ch'
        }
        from_page = self.request.POST.get('from_page')
        email_data = {
            'subject': "{dcl_text} Message from {sender}".format(
                dcl_text=settings.DCL_TEXT,
                sender=form.cleaned_data.get('email')
            ),
            'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': [from_emails.get(from_page, 'info@ungleich.ch')],
            'body': "\n".join(
                ["%s=%s" % (k, v) for (k, v) in form.cleaned_data.items()]),
            'reply_to': [form.cleaned_data.get('email')],
        }
        send_plain_email_task.delay(email_data)
        if self.request.is_ajax():
            return self.render_to_response(
                self.get_context_data(success=True, contact_form=form))
        else:
            return render(
                self.request, 'datacenterlight/index.html',
                self.get_context_data(success=True, contact_form=form)
            )


class IndexView(CreateView):
    template_name = "datacenterlight/index.html"
    success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def validate_cores(self, value):
        if (value > 48) or (value < 1):
            raise ValidationError(_('Invalid number of cores'))

    def validate_memory(self, value):
        if (value > 200) or (value < 1):
            raise ValidationError(_('Invalid RAM size'))

    def validate_storage(self, value):
        if (value > 2000) or (value < 10):
            raise ValidationError(_('Invalid storage size'))

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        for session_var in ['specs', 'user', 'billing_address_data',
                            'pricing_name']:
            if session_var in request.session:
                del request.session[session_var]
        return HttpResponseRedirect(reverse('datacenterlight:cms_index'))

    def post(self, request):
        cores = request.POST.get('cpu')
        cores_field = forms.IntegerField(validators=[self.validate_cores])
        memory = request.POST.get('ram')
        memory_field = forms.IntegerField(validators=[self.validate_memory])
        storage = request.POST.get('storage')
        storage_field = forms.IntegerField(validators=[self.validate_storage])
        template_id = int(request.POST.get('config'))
        pricing_name = request.POST.get('pricing_name')
        vm_pricing = VMPricing.get_vm_pricing_by_name(pricing_name)

        template = VMTemplate.objects.filter(
            opennebula_vm_template_id=template_id
        ).first()
        template_data = VMTemplateSerializer(template).data
        referer_url = request.META['HTTP_REFERER']

        if vm_pricing is None:
            vm_pricing_name_msg = _(
                "Incorrect pricing name. Please contact support"
                "{support_email}".format(
                    support_email=settings.DCL_SUPPORT_FROM_ADDRESS
                )
            )
            messages.add_message(
                self.request, messages.ERROR, vm_pricing_name_msg,
                extra_tags='pricing'
            )
            return HttpResponseRedirect(referer_url + "#order_form")
        else:
            vm_pricing_name = vm_pricing.name

        try:
            cores = cores_field.clean(cores)
        except ValidationError as err:
            msg = '{} : {}.'.format(cores, str(err))
            messages.add_message(
                self.request, messages.ERROR, msg, extra_tags='cores'
            )
            return HttpResponseRedirect(referer_url + "#order_form")

        try:
            memory = memory_field.clean(memory)
        except ValidationError as err:
            msg = '{} : {}.'.format(memory, str(err))
            messages.add_message(
                self.request, messages.ERROR, msg, extra_tags='memory'
            )
            return HttpResponseRedirect(referer_url + "#order_form")

        try:
            storage = storage_field.clean(storage)
        except ValidationError as err:
            msg = '{} : {}.'.format(storage, str(err))
            messages.add_message(
                self.request, messages.ERROR, msg, extra_tags='storage'
            )
            return HttpResponseRedirect(referer_url + "#order_form")

        price, vat, vat_percent, discount = get_vm_price_with_vat(
            cpu=cores,
            memory=memory,
            ssd_size=storage,
            pricing_name=vm_pricing_name
        )
        specs = {
            'cpu': cores,
            'memory': memory,
            'disk_size': storage,
            'price': price,
            'vat': vat,
            'vat_percent': vat_percent,
            'discount': discount,
            'total_price': price + vat - discount['amount'],
            'pricing_name': vm_pricing_name
        }
        request.session['specs'] = specs
        request.session['template'] = template_data
        return HttpResponseRedirect(reverse('datacenterlight:payment'))

    def get_success_url(self):
        success_url = reverse('datacenterlight:index')
        success_url += "#requestform"
        return success_url

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'base_url': "{0}://{1}".format(
                self.request.scheme, self.request.get_host()
            ),
            'contact_form': ContactForm
        })
        return context


class WhyDataCenterLightView(IndexView):
    template_name = "datacenterlight/whydatacenterlight.html"


class PaymentOrderView(FormView):
    template_name = 'datacenterlight/landing_payment.html'

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return BillingAddressForm
        else:
            return BillingAddressFormSignup

    def get_context_data(self, **kwargs):
        context = super(PaymentOrderView, self).get_context_data(**kwargs)
        if 'billing_address_data' in self.request.session:
            billing_address_data = self.request.session['billing_address_data']
        else:
            billing_address_data = {}

        if self.request.user.is_authenticated():
            if billing_address_data:
                billing_address_form = BillingAddressForm(
                    initial=billing_address_data
                )
            else:
                billing_address_form = BillingAddressForm(
                    instance=self.request.user.billing_addresses.first()
                )
            user = self.request.user
            if hasattr(user, 'stripecustomer'):
                stripe_customer = user.stripecustomer
            else:
                stripe_customer = None
            cards_list = UserCardDetail.get_all_cards_list(
                stripe_customer=stripe_customer
            )
            context.update({'cards_list': cards_list})
        else:
            billing_address_form = BillingAddressFormSignup(
                initial=billing_address_data
            )

        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY,
            'site_url': reverse('datacenterlight:index'),
            'login_form': HostingUserLoginForm(prefix='login_form'),
            'billing_address_form': billing_address_form,
            'cms_integration': get_cms_integration('default'),
        })

        if ('generic_payment_type' in self.request.session and
                self.request.session['generic_payment_type'] == 'generic'):
            if 'product_id' in self.request.session:
                product = GenericProduct.objects.get(
                    id=self.request.session['product_id']
                )
                context.update({'generic_payment_form': ProductPaymentForm(
                    prefix='generic_payment_form',
                    initial={'product_name': product.product_name,
                             'amount': float(product.get_actual_price()),
                             'recurring': product.product_is_subscription,
                             'description': product.product_description,
                             }
                ), })
            else:
                context.update({'generic_payment_form': GenericPaymentForm(
                    prefix='generic_payment_form',
                ), })
        else:
            context.update({
                'vm_pricing': VMPricing.get_vm_pricing_by_name(
                    self.request.session['specs']['pricing_name']
                )
            })

        return context

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if (('type' in request.GET and request.GET['type'] == 'generic')
                or 'product_slug' in kwargs):
            request.session['generic_payment_type'] = 'generic'
            if 'generic_payment_details' in request.session:
                request.session.pop('generic_payment_details')
                request.session.pop('product_id')
            if 'product_slug' in kwargs:
                logger.debug("Product slug is " + kwargs['product_slug'])
                try:
                    product = GenericProduct.objects.get(
                        product_slug=kwargs['product_slug']
                    )
                except GenericProduct.DoesNotExist as dne:
                    logger.error(
                        "Product '{}' does "
                        "not exist".format(kwargs['product_slug'])
                    )
                    raise Http404()
                request.session['product_id'] = product.id
        elif 'specs' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        if 'product' in request.POST:
            # query for the supplied product
            product = None
            try:
                product = GenericProduct.objects.get(
                    id=request.POST['generic_payment_form-product_name']
                )
            except GenericProduct.DoesNotExist as dne:
                logger.error(
                    "The requested product '{}' does not exist".format(
                        request.POST['generic_payment_form-product_name']
                    )
                )
            except GenericProduct.MultipleObjectsReturned as mpe:
                logger.error(
                    "There seem to be more than one product with "
                    "the name {}".format(
                        request.POST['generic_payment_form-product_name']
                    )
                )
                product = GenericProduct.objects.all(
                    product_name=request.
                    POST['generic_payment_form-product_name']
                ).first()
            if product is None:
                return JsonResponse({})
            else:
                return JsonResponse({
                    'amount': product.get_actual_price(),
                    'isSubscription': product.product_is_subscription
                })
        if 'login_form' in request.POST:
            login_form = HostingUserLoginForm(
                data=request.POST, prefix='login_form'
            )
            if login_form.is_valid():
                email = login_form.cleaned_data.get('email')
                password = login_form.cleaned_data.get('password')
                auth_user = authenticate(email=email, password=password)
                if auth_user:
                    login(self.request, auth_user)
                    return HttpResponseRedirect(
                        reverse('datacenterlight:payment')
                    )
            else:
                context = self.get_context_data()
                context['login_form'] = login_form
                return self.render_to_response(context)
        if request.user.is_authenticated():
            address_form = BillingAddressForm(
                data=request.POST,
            )
        else:
            address_form = BillingAddressFormSignup(
                data=request.POST,
            )
        if address_form.is_valid():
            # Check if we are in a generic payment case and handle the generic
            # payment details form before we go on to verify payment
            if ('generic_payment_type' in request.session and
                    self.request.session['generic_payment_type'] == 'generic'):
                generic_payment_form = GenericPaymentForm(
                    data=request.POST, prefix='generic_payment_form'
                )
                if generic_payment_form.is_valid():
                    logger.debug("Generic payment form is valid.")
                    product = generic_payment_form.cleaned_data.get(
                        'product_name'
                    )
                    gp_details = {
                        "product_name": product.product_name,
                        "amount": generic_payment_form.cleaned_data.get(
                            'amount'
                        ),
                        "recurring": generic_payment_form.cleaned_data.get(
                            'recurring'
                        ),
                        "description": generic_payment_form.cleaned_data.get(
                            'description'
                        ),
                        "product_id": product.id
                    }
                    request.session["generic_payment_details"] = (
                        gp_details
                    )
                else:
                    logger.debug("Generic payment form invalid")
                    context = self.get_context_data()
                    context['generic_payment_form'] = generic_payment_form
                    context['billing_address_form'] = address_form
                    return self.render_to_response(context)
            token = address_form.cleaned_data.get('token')
            if token is '':
                card_id = address_form.cleaned_data.get('card')
                try:
                    user_card_detail = UserCardDetail.objects.get(id=card_id)
                    if not request.user.has_perm(
                            'view_usercarddetail', user_card_detail
                    ):
                        raise UserCardDetail.DoesNotExist(
                            _("{user} does not have permission to access the "
                              "card").format(user=request.user.email)
                        )
                except UserCardDetail.DoesNotExist as e:
                    ex = str(e)
                    logger.error("Card Id: {card_id}, Exception: {ex}".format(
                        card_id=card_id, ex=ex
                    )
                    )
                    msg = _("An error occurred. Details: {}".format(ex))
                    messages.add_message(
                        self.request, messages.ERROR, msg,
                        extra_tags='make_charge_error'
                    )
                    return HttpResponseRedirect(
                        reverse('datacenterlight:payment') + '#payment_error'
                    )
                request.session['card_id'] = user_card_detail.id
            else:
                request.session['token'] = token
            if request.user.is_authenticated():
                this_user = {
                    'email': request.user.email,
                    'name': request.user.name
                }
                customer = StripeCustomer.get_or_create(
                    email=this_user.get('email'), token=token
                )
            else:
                user_email = address_form.cleaned_data.get('email')
                user_name = address_form.cleaned_data.get('name')
                this_user = {
                    'email': user_email,
                    'name': user_name
                }
                try:
                    custom_user = CustomUser.objects.get(email=user_email)
                    customer = StripeCustomer.objects.filter(
                        user_id=custom_user.id).first()
                    if customer is None:
                        logger.debug(
                            ("User {email} is already registered with us."
                             "But, StripeCustomer does not exist for {email}."
                             "Hence, creating a new StripeCustomer.").format(
                                email=user_email
                            )
                        )
                        customer = StripeCustomer.create_stripe_api_customer(
                            email=user_email,
                            token=token,
                            customer_name=user_name)
                except CustomUser.DoesNotExist:
                    logger.debug(
                        ("StripeCustomer does not exist for {email}."
                         "Hence, creating a new StripeCustomer.").format(
                            email=user_email
                        )
                    )
                    customer = StripeCustomer.create_stripe_api_customer(
                        email=user_email,
                        token=token,
                        customer_name=user_name)

            request.session['billing_address_data'] = address_form.cleaned_data
            request.session['user'] = this_user
            # Get or create stripe customer
            if not customer:
                address_form.add_error(
                    "__all__", "Invalid credit card"
                )
                return self.render_to_response(
                    self.get_context_data(
                        billing_address_form=address_form
                    )
                )
            if type(customer) is StripeCustomer:
                request.session['customer'] = customer.stripe_id
            else:
                request.session['customer'] = customer
            return HttpResponseRedirect(
                reverse('datacenterlight:order_confirmation'))
        else:
            context = self.get_context_data()
            context['billing_address_form'] = address_form
            return self.render_to_response(context)


class OrderConfirmationView(DetailView):
    template_name = "datacenterlight/order_detail.html"
    payment_template_name = 'datacenterlight/landing_payment.html'
    context_object_name = "order"
    model = HostingOrder

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        context = {}
        if (('specs' not in request.session or 'user' not in request.session)
                and 'generic_payment_type' not in request.session):
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        if 'token' in self.request.session:
            token = self.request.session['token']
            stripe_utils = StripeUtils()
            card_details = stripe_utils.get_cards_details_from_token(
                token
            )
            if not card_details.get('response_object'):
                return HttpResponseRedirect(reverse('hosting:payment'))
            card_details_response = card_details['response_object']
            context['cc_last4'] = card_details_response['last4']
            context['cc_brand'] = card_details_response['brand']
        else:
            card_id = self.request.session.get('card_id')
            card_detail = UserCardDetail.objects.get(id=card_id)
            context['cc_last4'] = card_detail.last4
            context['cc_brand'] = card_detail.brand

        if ('generic_payment_type' in request.session and
                self.request.session['generic_payment_type'] == 'generic'):
            context.update({
                'generic_payment_details':
                    request.session['generic_payment_details'],
            })
        else:
            context.update({
                'vm': request.session.get('specs'),
            })
        context.update({
            'site_url': reverse('datacenterlight:index'),
            'page_header_text': _('Confirm Order'),
            'billing_address_data': (
                request.session.get('billing_address_data')
            ),
            'cms_integration': get_cms_integration('default'),
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        user = request.session.get('user')
        stripe_api_cus_id = request.session.get('customer')
        stripe_utils = StripeUtils()

        if 'token' in request.session:
            card_details = stripe_utils.get_cards_details_from_token(
                request.session.get('token')
            )
            if not card_details.get('response_object'):
                msg = card_details.get('error')
                messages.add_message(self.request, messages.ERROR, msg,
                                     extra_tags='failed_payment')
                response = {
                    'status': False,
                    'redirect': "{url}#{section}".format(
                        url=reverse('datacenterlight:payment'),
                        section='payment_error'),
                    'msg_title': str(_('Error.')),
                    'msg_body': str(
                        _('There was a payment related error.'
                          ' On close of this popup, you will be'
                          ' redirected back to the payment page.')
                    )
                }
                return JsonResponse(response)
            card_details_response = card_details['response_object']
            card_details_dict = {
                'last4': card_details_response['last4'],
                'brand': card_details_response['brand'],
                'card_id': card_details_response['card_id']
            }
            stripe_customer_obj = StripeCustomer.objects.filter(
                stripe_id=stripe_api_cus_id).first()
            if stripe_customer_obj:
                ucd = UserCardDetail.get_user_card_details(
                    stripe_customer_obj, card_details_response
                )
                if not ucd:
                    acc_result = stripe_utils.associate_customer_card(
                        stripe_api_cus_id, request.session['token'],
                        set_as_default=True
                    )
                    if acc_result['response_object'] is None:
                        msg = _(
                            'An error occurred while associating the card.'
                            ' Details: {details}'.format(
                                details=acc_result['error']
                            )
                        )
                        messages.add_message(self.request, messages.ERROR, msg,
                                             extra_tags='failed_payment')
                        response = {
                            'status': False,
                            'redirect': "{url}#{section}".format(
                                url=reverse('hosting:payment'),
                                section='payment_error'),
                            'msg_title': str(_('Error.')),
                            'msg_body': str(
                                _('There was a payment related error.'
                                  ' On close of this popup, you will be redirected'
                                  ' back to the payment page.')
                            )
                        }
                        return JsonResponse(response)
        elif 'card_id' in request.session:
            card_id = request.session.get('card_id')
            user_card_detail = UserCardDetail.objects.get(id=card_id)
            card_details_dict = {
                'last4': user_card_detail.last4,
                'brand': user_card_detail.brand,
                'card_id': user_card_detail.card_id
            }
        else:
            response = {
                'status': False,
                'redirect': "{url}#{section}".format(
                    url=reverse('datacenterlight:payment'),
                    section='payment_error'),
                'msg_title': str(_('Error.')),
                'msg_body': str(
                    _('There was a payment related error.'
                      ' On close of this popup, you will be redirected back to'
                      ' the payment page.'))
            }
            return JsonResponse(response)

        if ('generic_payment_type' in request.session and
                self.request.session['generic_payment_type'] == 'generic'):
            gp_details = self.request.session['generic_payment_details']
            if gp_details['recurring']:
                # generic recurring payment
                logger.debug("Commencing a generic recurring payment")
            else:
                # generic one time payment
                logger.debug("Commencing a one time payment")
                charge_response = stripe_utils.make_charge(
                    amount=gp_details['amount'],
                    customer=stripe_api_cus_id
                )
                stripe_onetime_charge = charge_response.get('response_object')

                # Check if the payment was approved
                if not stripe_onetime_charge:
                    msg = charge_response.get('error')
                    messages.add_message(self.request, messages.ERROR, msg,
                                         extra_tags='failed_payment')
                    response = {
                        'status': False,
                        'redirect': "{url}#{section}".format(
                            url=(reverse('datacenterlight:payment') +
                                 "?type=generic"),
                            section='payment_error'),
                        'msg_title': str(_('Error.')),
                        'msg_body': str(
                            _('There was a payment related error.'
                              ' On close of this popup, you will be redirected'
                              ' back to the payment page.'))
                    }
                    return JsonResponse(response)

        if ('generic_payment_type' not in request.session or
                (request.session['generic_payment_details']['recurring'])):
            if 'generic_payment_details' in request.session:
                amount_to_be_charged = (
                    round(
                        request.session['generic_payment_details']['amount'],
                        2
                    )
                )
                plan_name = "generic-{0}-{1:.2f}".format(
                    request.session['generic_payment_details']['product_id'],
                    amount_to_be_charged
                )
                stripe_plan_id = plan_name
            else:
                template = request.session.get('template')
                specs = request.session.get('specs')
                vm_template_id = template.get('id', 1)

                cpu = specs.get('cpu')
                memory = specs.get('memory')
                disk_size = specs.get('disk_size')
                amount_to_be_charged = specs.get('total_price')
                plan_name = StripeUtils.get_stripe_plan_name(
                    cpu=cpu,
                    memory=memory,
                    disk_size=disk_size,
                    price=amount_to_be_charged
                )
                stripe_plan_id = StripeUtils.get_stripe_plan_id(
                    cpu=cpu,
                    ram=memory,
                    ssd=disk_size,
                    version=1,
                    app='dcl',
                    price=amount_to_be_charged
                )
            stripe_plan = stripe_utils.get_or_create_stripe_plan(
                amount=amount_to_be_charged,
                name=plan_name,
                stripe_plan_id=stripe_plan_id)
            subscription_result = stripe_utils.subscribe_customer_to_plan(
                stripe_api_cus_id,
                [{"plan": stripe_plan.get(
                    'response_object').stripe_plan_id}])
            stripe_subscription_obj = subscription_result.get('response_object')
            # Check if the subscription was approved and is active
            if (stripe_subscription_obj is None
                    or stripe_subscription_obj.status != 'active'):
                # At this point, we have created a Stripe API card and
                # associated it with the customer; but the transaction failed
                # due to some reason. So, we would want to dissociate this card
                # here.
                # ...

                msg = subscription_result.get('error')
                messages.add_message(self.request, messages.ERROR, msg,
                                     extra_tags='failed_payment')
                response = {
                    'status': False,
                    'redirect': "{url}#{section}".format(
                        url=reverse('datacenterlight:payment'),
                        section='payment_error'),
                    'msg_title': str(_('Error.')),
                    'msg_body': str(
                        _('There was a payment related error.'
                          ' On close of this popup, you will be redirected back to'
                          ' the payment page.'))
                }
                return JsonResponse(response)

        # Create user if the user is not logged in and if he is not already
        # registered
        if not request.user.is_authenticated():
            try:
                custom_user = CustomUser.objects.get(
                    email=user.get('email'))
                stripe_customer = StripeCustomer.objects.filter(
                    user_id=custom_user.id).first()
                if stripe_customer is None:
                    stripe_customer = StripeCustomer.objects.create(
                        user=custom_user, stripe_id=stripe_api_cus_id
                    )
                stripe_customer_id = stripe_customer.id
            except CustomUser.DoesNotExist:
                logger.debug(
                    "Customer {} does not exist.".format(user.get('email')))
                password = CustomUser.get_random_password()
                base_url = "{0}://{1}".format(self.request.scheme,
                                              self.request.get_host())
                custom_user = CustomUser.register(
                    user.get('name'), password,
                    user.get('email'),
                    app='dcl', base_url=base_url, send_email=True,
                    account_details=password
                )
                logger.debug("Created user {}.".format(user.get('email')))
                stripe_customer = StripeCustomer.objects. \
                    create(user=custom_user, stripe_id=stripe_api_cus_id)
                stripe_customer_id = stripe_customer.id
                new_user = authenticate(username=custom_user.email,
                                        password=password)
                login(request, new_user)
        else:
            # We assume that if the user is here, his/her StripeCustomer
            # object already exists
            stripe_customer_id = request.user.stripecustomer.id
            custom_user = request.user

        if 'token' in request.session:
            ucd = UserCardDetail.get_or_create_user_card_detail(
                stripe_customer=self.request.user.stripecustomer,
                card_details=card_details_response
            )
            UserCardDetail.save_default_card_local(
                self.request.user.stripecustomer.stripe_id,
                ucd.card_id
            )
        else:
            card_id = request.session.get('card_id')
            user_card_detail = UserCardDetail.objects.get(id=card_id)
            card_details_dict = {
                'last4': user_card_detail.last4,
                'brand': user_card_detail.brand,
                'card_id': user_card_detail.card_id
            }
            if not user_card_detail.preferred:
                UserCardDetail.set_default_card(
                    stripe_api_cus_id=stripe_api_cus_id,
                    stripe_source_id=user_card_detail.card_id
                )

        # Save billing address
        billing_address_data = request.session.get('billing_address_data')
        logger.debug('billing_address_data is {}'.format(billing_address_data))
        billing_address_data.update({
            'user': custom_user.id
        })

        if 'generic_payment_type' in request.session:
            stripe_cus = StripeCustomer.objects.filter(
                stripe_id=stripe_api_cus_id
            ).first()
            billing_address = BillingAddress(
                cardholder_name=billing_address_data['cardholder_name'],
                street_address=billing_address_data['street_address'],
                city=billing_address_data['city'],
                postal_code=billing_address_data['postal_code'],
                country=billing_address_data['country']
            )
            billing_address.save()

            order = HostingOrder.create(
                price=self.request
                          .session['generic_payment_details']['amount'],
                customer=stripe_cus,
                billing_address=billing_address,
                vm_pricing=VMPricing.get_default_pricing()
            )

            # Create a Hosting Bill
            HostingBill.create(customer=stripe_cus,
                               billing_address=billing_address)

            # Create Billing Address for User if he does not have one
            if not stripe_cus.user.billing_addresses.count():
                billing_address_data.update({
                    'user': stripe_cus.user.id
                })
                billing_address_user_form = UserBillingAddressForm(
                    billing_address_data
                )
                billing_address_user_form.is_valid()
                billing_address_user_form.save()

            if self.request.session['generic_payment_details']['recurring']:
                # Associate the given stripe subscription with the order
                order.set_subscription_id(
                    stripe_subscription_obj.id, card_details_dict
                )
            else:
                # Associate the given stripe charge id with the order
                order.set_stripe_charge(stripe_onetime_charge)

            # Set order status approved
            order.set_approved()
            order.generic_payment_description = gp_details["description"]
            order.generic_product_id = gp_details["product_id"]
            order.save()
            # send emails
            context = {
                'name': user.get('name'),
                'email': user.get('email'),
                'amount': gp_details['amount'],
                'description': gp_details['description'],
                'recurring': gp_details['recurring'],
                'product_name': gp_details['product_name'],
                'product_id': gp_details['product_id'],
                'order_id': order.id
            }

            email_data = {
                'subject': (settings.DCL_TEXT +
                            " Payment received from %s" % context['email']),
                'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
                'to': ['info@ungleich.ch'],
                'body': "\n".join(
                    ["%s=%s" % (k, v) for (k, v) in context.items()]),
                'reply_to': [context['email']],
            }
            send_plain_email_task.delay(email_data)

            email_data = {
                'subject': _("Confirmation of your payment"),
                'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
                'to': [user.get('email')],
                'body': _("Hi {name},\n\n"
                          "thank you for your order!\n"
                          "We have just received a payment of CHF {amount:.2f}"
                          " from you.{recurring}\n\n"
                          "Cheers,\nYour Data Center Light team".format(
                                 name=user.get('name'),
                                 amount=gp_details['amount'],
                                 recurring=(
                                     _(' This is a monthly recurring plan.')
                                     if gp_details['recurring'] else ''
                                 )
                             )
                          ),
                'reply_to': ['info@ungleich.ch'],
            }
            send_plain_email_task.delay(email_data)

            response = {
                'status': True,
                'redirect': (
                    reverse('hosting:orders')
                    if request.user.is_authenticated()
                    else reverse('datacenterlight:index')
                ),
                'msg_title': str(_('Thank you for the payment.')),
                'msg_body': str(
                    _('You will soon receive a confirmation email of the '
                      'payment. You can always contact us at '
                      'info@ungleich.ch for any question that you may have.')
                )
            }
            for session_var in ['specs', 'template', 'billing_address',
                                'billing_address_data', 'card_id',
                                'token', 'customer', 'generic_payment_type',
                                'generic_payment_details', 'product_id']:
                if session_var in request.session:
                    del request.session[session_var]

            return JsonResponse(response)

        user = {
            'name': custom_user.name,
            'email': custom_user.email,
            'pass': custom_user.password,
            'request_scheme': request.scheme,
            'request_host': request.get_host(),
            'language': get_language(),
        }

        create_vm(
            billing_address_data, stripe_customer_id, specs,
            stripe_subscription_obj, card_details_dict, request,
            vm_template_id, template, user
        )

        response = {
            'status': True,
            'redirect': (
                reverse('hosting:virtual_machines')
                if request.user.is_authenticated()
                else reverse('datacenterlight:index')
            ),
            'msg_title': str(_('Thank you for the order.')),
            'msg_body': str(
                _('Your VM will be up and running in a few moments.'
                  ' We will send you a confirmation email as soon as'
                  ' it is ready.'))
        }

        return JsonResponse(response)

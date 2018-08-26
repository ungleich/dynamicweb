import logging

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.utils.translation import get_language, ugettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, CreateView, DetailView

from hosting.forms import HostingUserLoginForm
from hosting.models import HostingOrder, UserCardDetail
from membership.models import CustomUser, StripeCustomer
from opennebula_api.serializers import VMTemplateSerializer
from utils.forms import BillingAddressForm, BillingAddressFormSignup
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
            'vm_pricing': VMPricing.get_vm_pricing_by_name(
                self.request.session['specs']['pricing_name']
            )
        })
        return context

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if 'specs' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
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
        if 'specs' not in request.session or 'user' not in request.session:
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
        context.update({
            'site_url': reverse('datacenterlight:index'),
            'vm': request.session.get('specs'),
            'page_header_text': _('Confirm Order'),
            'billing_address_data': (
                request.session.get('billing_address_data')
            ),
            'cms_integration': get_cms_integration('default'),
        })
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        template = request.session.get('template')
        specs = request.session.get('specs')
        user = request.session.get('user')
        stripe_api_cus_id = request.session.get('customer')
        vm_template_id = template.get('id', 1)
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
            stripe_customer_obj = StripeCustomer.objects.filter(stripe_id=stripe_api_cus_id).first()
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

        cpu = specs.get('cpu')
        memory = specs.get('memory')
        disk_size = specs.get('disk_size')
        amount_to_be_charged = specs.get('total_price')
        plan_name = StripeUtils.get_stripe_plan_name(cpu=cpu,
                                                     memory=memory,
                                                     disk_size=disk_size)
        stripe_plan_id = StripeUtils.get_stripe_plan_id(cpu=cpu,
                                                        ram=memory,
                                                        ssd=disk_size,
                                                        version=1,
                                                        app='dcl')
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

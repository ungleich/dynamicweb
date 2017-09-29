import logging
import json

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render
from django.utils.translation import get_language, ugettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, CreateView, TemplateView, DetailView

from datacenterlight.tasks import create_vm_task
from hosting.models import HostingOrder
from hosting.forms import HostingUserLoginForm
from membership.models import CustomUser, StripeCustomer
from opennebula_api.serializers import VMTemplateSerializer
from utils.forms import (
    BillingAddressForm, BillingAddressFormSignup, UserBillingAddressForm
)
from utils.hosting_utils import get_vm_price
from utils.mailer import BaseEmail
from utils.stripe_utils import StripeUtils
from utils.tasks import send_plain_email_task
from .forms import BetaAccessForm, ContactForm
from .models import BetaAccess, BetaAccessVMType, BetaAccessVM, VMTemplate

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
            return render(self.request,
                          'datacenterlight/index.html',
                          self.get_context_data(contact_form=form))

    def form_valid(self, form):
        form.save()
        email_data = {
            'subject': "{dcl_text} Message from {sender}".format(
                dcl_text=settings.DCL_TEXT,
                sender=form.cleaned_data.get('email')
            ),
            'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': ['info@ungleich.ch'],
            'body': "\n".join(
                ["%s=%s" % (k, v) for (k, v) in form.cleaned_data.items()]),
            'reply_to': [form.cleaned_data.get('email')],
        }
        send_plain_email_task.delay(email_data)
        if self.request.is_ajax():
            return self.render_to_response(
                self.get_context_data(success=True, contact_form=form))
        else:
            return render(self.request,
                          'datacenterlight/index.html',
                          self.get_context_data(success=True,
                                                contact_form=form))


class LandingProgramView(TemplateView):
    template_name = "datacenterlight/landing.html"


class SuccessView(TemplateView):
    template_name = "datacenterlight/success.html"

    def get(self, request, *args, **kwargs):
        if 'specs' not in request.session or 'user' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        elif 'token' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:payment'))
        elif 'order_confirmation' not in request.session:
            return HttpResponseRedirect(
                reverse('datacenterlight:order_confirmation'))
        else:
            for session_var in ['specs', 'user', 'template', 'billing_address',
                                'billing_address_data',
                                'token', 'customer']:
                if session_var in request.session:
                    del request.session[session_var]
        return render(request, self.template_name)


class BetaAccessView(FormView):
    template_name = "datacenterlight/beta_access.html"
    form_class = BetaAccessForm
    success_message = "Thank you, we will contact you as soon as possible"

    def form_valid(self, form):
        context = {
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host())
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'from_address': '(datacenterlight) datacenterlight Support <support@datacenterlight.ch>',
            'to': form.cleaned_data.get('email'),
            'from': '(datacenterlight) DatacenterLight Support support@datacenterlight.ch',
            'context': context,
            'template_name': 'request_access_confirmation',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        context.update({
            'email': form.cleaned_data.get('email')
        })

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'from_address': '(datacenterlight) datacenterlight Support <support@datacenterlight.ch>',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS,
                             self.success_message)
        return render(self.request, 'datacenterlight/beta_success.html', {})


class BetaProgramView(CreateView):
    template_name = "datacenterlight/beta.html"
    model = BetaAccessVM
    fields = '__all__'
    # form_class = BetaAccessForm
    # success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def get_success_url(self):
        success_url = reverse('datacenterlight:beta')
        success_url += "#success"
        return success_url

    def get_context_data(self, **kwargs):
        vms = BetaAccessVMType.objects.all()
        context = super(BetaProgramView, self).get_context_data(**kwargs)

        # templates = OpenNebulaManager().get_templates()
        # data = VirtualMachineTemplateSerializer(templates, many=True).data

        context.update({
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host()),
            'vms': vms
        })
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vms = BetaAccessVM.create(data)

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host()),
            'email': data.get('email'),
            'name': data.get('name'),
            'vms': vms
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'from_address': '(datacenterlight) datacenterlight Support <support@datacenterlight.ch>',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_beta_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS,
                             self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class IndexView(CreateView):
    template_name = "datacenterlight/index.html"
    model = BetaAccess
    form_class = BetaAccessForm
    success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def validate_cores(self, value):
        if (value > 48) or (value < 1):
            raise ValidationError(_('Invalid number of cores'))

    def validate_memory(self, value):
        if (value > 200) or (value < 2):
            raise ValidationError(_('Invalid RAM size'))

    def validate_storage(self, value):
        if (value > 2000) or (value < 10):
            raise ValidationError(_('Invalid storage size'))

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        for session_var in ['specs', 'user', 'billing_address_data']:
            if session_var in request.session:
                del request.session[session_var]

        vm_templates = VMTemplate.objects.all()
        context = {
            'templates': vm_templates
        }
        return render(request, self.template_name, context)

    def post(self, request):
        cores = request.POST.get('cpu')
        cores_field = forms.IntegerField(validators=[self.validate_cores])
        memory = request.POST.get('ram')
        memory_field = forms.IntegerField(validators=[self.validate_memory])
        storage = request.POST.get('storage')
        storage_field = forms.IntegerField(validators=[self.validate_storage])
        template_id = int(request.POST.get('config'))
        template = VMTemplate.objects.filter(
            opennebula_vm_template_id=template_id).first()
        template_data = VMTemplateSerializer(template).data

        try:
            cores = cores_field.clean(cores)
        except ValidationError as err:
            msg = '{} : {}.'.format(cores, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='cores')
            return HttpResponseRedirect(
                reverse('datacenterlight:index') + "#order_form")

        try:
            memory = memory_field.clean(memory)
        except ValidationError as err:
            msg = '{} : {}.'.format(memory, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='memory')
            return HttpResponseRedirect(
                reverse('datacenterlight:index') + "#order_form")

        try:
            storage = storage_field.clean(storage)
        except ValidationError as err:
            msg = '{} : {}.'.format(storage, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='storage')
            return HttpResponseRedirect(
                reverse('datacenterlight:index') + "#order_form")
        amount_to_be_charged = get_vm_price(cpu=cores, memory=memory,
                                            disk_size=storage)
        specs = {
            'cpu': cores,
            'memory': memory,
            'disk_size': storage,
            'price': amount_to_be_charged
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
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host()),
            'contact_form': ContactForm
        })
        return context

    def form_valid(self, form):

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host())
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'from_address': '(datacenterlight) datacenterlight Support <support@datacenterlight.ch>',
            'to': form.cleaned_data.get('email'),
            'from': '(datacenterlight) DatacenterLight Support support@datacenterlight.ch',
            'context': context,
            'template_name': 'request_access_confirmation',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        context.update({
            'email': form.cleaned_data.get('email')
        })

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'from_address': '(datacenterlight) datacenterlight Support <support@datacenterlight.ch>',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS,
                             self.success_message)
        return super(IndexView, self).form_valid(form)


class WhyDataCenterLightView(IndexView):
    template_name = "datacenterlight/whydatacenterlight.html"
    model = BetaAccess


class PaymentOrderView(FormView):
    template_name = 'datacenterlight/landing_payment.html'

    def get_form_class(self):
        if self.request.user.is_authenticated():
            return BillingAddressForm
        else:
            return BillingAddressFormSignup

    def get_form_kwargs(self):
        form_kwargs = super(PaymentOrderView, self).get_form_kwargs()
        # if user is signed in, get billing address
        if self.request.user.is_authenticated():
            form_kwargs.update({
                'instance': self.request.user.billing_addresses.first()
            })
        if 'billing_address_data' in self.request.session:
            billing_address_data = self.request.session['billing_address_data']
            form_kwargs.update({
                'initial': billing_address_data
            })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(PaymentOrderView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY,
            'site_url': reverse('datacenterlight:index'),
            'login_form': HostingUserLoginForm()
        })
        return context

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        # user is no longer added to session on the index page
        if 'specs' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            token = form.cleaned_data.get('token')
            if request.user.is_authenticated():
                this_user = {
                    'email': request.user.email,
                    'name': request.user.name
                }
                customer = StripeCustomer.get_or_create(
                    email=this_user.get('email'),
                    token=token)
            else:
                user_email = form.cleaned_data.get('email')
                user_name = form.cleaned_data.get('name')
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

            request.session['billing_address_data'] = form.cleaned_data
            request.session['user'] = this_user
            # Get or create stripe customer
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(
                    self.get_context_data(form=form))
            request.session['token'] = token
            if type(customer) is StripeCustomer:
                request.session['customer'] = customer.stripe_id
            else:
                request.session['customer'] = customer
            return HttpResponseRedirect(
                reverse('datacenterlight:order_confirmation'))
        else:
            return self.form_invalid(form)


class OrderConfirmationView(DetailView):
    template_name = "datacenterlight/order_detail.html"
    payment_template_name = 'datacenterlight/landing_payment.html'
    context_object_name = "order"
    model = HostingOrder

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if 'specs' not in request.session or 'user' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        if 'token' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:payment'))
        stripe_api_cus_id = request.session.get('customer')
        stripe_utils = StripeUtils()
        card_details = stripe_utils.get_card_details(stripe_api_cus_id,
                                                     request.session.get(
                                                         'token'))
        if not card_details.get('response_object'):
            msg = card_details.get('error')
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='failed_payment')
            return HttpResponseRedirect(
                reverse('datacenterlight:payment') + '#payment_error')
        context = {
            'site_url': reverse('datacenterlight:index'),
            'cc_last4': card_details.get('response_object').get('last4'),
            'cc_brand': card_details.get('response_object').get('brand'),
            'billing_address_data': request.session.get('billing_address_data')
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        template = request.session.get('template')
        specs = request.session.get('specs')
        user = request.session.get('user')
        stripe_api_cus_id = request.session.get('customer')
        vm_template_id = template.get('id', 1)
        stripe_utils = StripeUtils()
        card_details = stripe_utils.get_card_details(stripe_api_cus_id,
                                                     request.session.get(
                                                         'token'))
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
                      ' On close of this popup, you will be redirected back to'
                      ' the payment page.'))
            }
            return HttpResponse(json.dumps(response),
                                content_type="application/json")
        card_details_dict = card_details.get('response_object')
        cpu = specs.get('cpu')
        memory = specs.get('memory')
        disk_size = specs.get('disk_size')
        amount_to_be_charged = specs.get('price')
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
        if stripe_subscription_obj is None or \
                        stripe_subscription_obj.status != 'active':
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
                      ' Details: {error_detail}.'
                      ' On close of this popup, you will be redirected back to'
                      ' the payment page.'.format(error_detail=msg)))
            }
            return HttpResponse(json.dumps(response),
                                content_type="application/json")

        # Create user if the user is not logged in and if he is not already
        # registered
        if not request.user.is_authenticated():
            try:
                custom_user = CustomUser.objects.get(
                    email=user.get('email'))
                customer = StripeCustomer.objects.filter(
                    user_id=custom_user.id).first()
                stripe_customer_id = customer.id
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

        # Save billing address
        billing_address_data = request.session.get('billing_address_data')
        logger.debug('billing_address_data is {}'.format(billing_address_data))
        billing_address_data.update({
            'user': custom_user.id
        })
        billing_address_user_form = UserBillingAddressForm(
            instance=custom_user.billing_addresses.first(),
            data=billing_address_data)
        billing_address = billing_address_user_form.save()
        billing_address_id = billing_address.id
        logger.debug("billing address id = {}".format(billing_address_id))
        user = {
            'name': custom_user.name,
            'email': custom_user.email,
            'pass': custom_user.password,
            'request_scheme': request.scheme,
            'request_host': request.get_host(),
            'language': get_language(),
        }

        create_vm_task.delay(vm_template_id, user, specs, template,
                             stripe_customer_id, billing_address_data,
                             billing_address_id,
                             stripe_subscription_obj.id, card_details_dict)
        for session_var in ['specs', 'template', 'billing_address',
                            'billing_address_data',
                            'token', 'customer']:
            if session_var in request.session:
                del request.session[session_var]

        response = {
            'status': True,
            'redirect': reverse(
                'hosting:virtual_machines') if request.user.is_authenticated() else reverse(
                'datacenterlight:index'),
            'msg_title': str(_('Thank you for the order.')),
            'msg_body': str(
                _('Your VM will be up and running in a few moments.'
                  ' We will send you a confirmation email as soon as'
                  ' it is ready.'))
        }

        return HttpResponse(json.dumps(response),
                            content_type="application/json")

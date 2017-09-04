from django import forms
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.translation import ugettext_lazy as _
from django.views.decorators.cache import cache_control
from django.views.generic import FormView, CreateView, TemplateView, DetailView

from datacenterlight.tasks import create_vm_task
from hosting.models import HostingOrder
from membership.models import CustomUser, StripeCustomer
from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineTemplateSerializer, \
    VMTemplateSerializer
from utils.forms import BillingAddressForm
from utils.mailer import BaseEmail
from utils.stripe_utils import StripeUtils
from utils.tasks import send_plain_email_task
from .forms import BetaAccessForm, ContactForm
from .models import BetaAccess, BetaAccessVMType, BetaAccessVM, VMTemplate


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


class PricingView(TemplateView):
    template_name = "datacenterlight/pricing.html"

    def get(self, request, *args, **kwargs):
        try:
            manager = OpenNebulaManager()
            templates = manager.get_templates()

            context = {
                'templates': VirtualMachineTemplateSerializer(templates,
                                                              many=True).data,
            }
        except:
            messages.error(request,
                           'We have a temporary problem to connect to our backend. \
                           Please try again in a few minutes'
                           )
            context = {
                'error': 'connection'
            }

        return render(request, self.template_name, context)

    def post(self, request):

        cores = request.POST.get('cpu')
        memory = request.POST.get('ram')
        storage = request.POST.get('storage')
        price = request.POST.get('total')

        template_id = int(request.POST.get('config'))
        manager = OpenNebulaManager()
        template = manager.get_template(template_id)

        request.session['template'] = VirtualMachineTemplateSerializer(
            template).data

        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')

        request.session['specs'] = {
            'cpu': cores,
            'memory': memory,
            'disk_size': storage,
            'price': price,
        }

        return redirect(reverse('hosting:payment'))


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
        price = request.POST.get('total')
        template_id = int(request.POST.get('config'))
        template = VMTemplate.objects.filter(
            opennebula_vm_template_id=template_id).first()
        template_data = VMTemplateSerializer(template).data

        name = request.POST.get('name')
        email = request.POST.get('email')
        name_field = forms.CharField()
        email_field = forms.EmailField()

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

        try:
            name = name_field.clean(name)
        except ValidationError as err:
            msg = '{} {}.'.format(name, _('is not a proper name'))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='name')
            return HttpResponseRedirect(
                reverse('datacenterlight:index') + "#order_form")

        try:
            email = email_field.clean(email)
        except ValidationError as err:
            msg = '{} {}.'.format(email, _('is not a proper email'))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='email')
            return HttpResponseRedirect(
                reverse('datacenterlight:index') + "#order_form")

        specs = {
            'cpu': cores,
            'memory': memory,
            'disk_size': storage,
            'price': price
        }

        this_user = {
            'name': name,
            'email': email
        }

        request.session['specs'] = specs
        request.session['template'] = template_data
        request.session['user'] = this_user
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
    form_class = BillingAddressForm

    def get_form_kwargs(self):
        form_kwargs = super(PaymentOrderView, self).get_form_kwargs()
        billing_address_data = self.request.session.get('billing_address_data')
        if billing_address_data:
            form_kwargs.update({
                'initial': {
                    'cardholder_name': billing_address_data['cardholder_name'],
                    'street_address': billing_address_data['street_address'],
                    'city': billing_address_data['city'],
                    'postal_code': billing_address_data['postal_code'],
                    'country': billing_address_data['country'],
                }
            })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(PaymentOrderView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY,
            'site_url': reverse('datacenterlight:index')
        })
        return context

    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if 'specs' not in request.session or 'user' not in request.session:
            return HttpResponseRedirect(reverse('datacenterlight:index'))
        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Get billing address data
            billing_address_data = form.cleaned_data
            token = form.cleaned_data.get('token')
            user = request.session.get('user')
            try:
                CustomUser.objects.get(email=user.get('email'))
            except CustomUser.DoesNotExist:
                password = CustomUser.get_random_password()
                # Register the user, and do not send emails
                CustomUser.register(user.get('name'),
                                    password,
                                    user.get('email'),
                                    app='dcl',
                                    base_url=None, send_email=False)

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=user.get('email'),
                                                    token=token)
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(
                    self.get_context_data(form=form))

            # Create Billing Address
            billing_address = form.save()
            request.session['billing_address_data'] = billing_address_data
            request.session['billing_address'] = billing_address.id
            request.session['token'] = token
            request.session['customer'] = customer.id
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
        stripe_customer_id = request.session.get('customer')
        customer = StripeCustomer.objects.filter(id=stripe_customer_id).first()
        stripe_utils = StripeUtils()
        card_details = stripe_utils.get_card_details(customer.stripe_id,
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
            'cc_brand': card_details.get('response_object').get('brand')
        }
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        template = request.session.get('template')
        specs = request.session.get('specs')
        user = request.session.get('user')
        stripe_customer_id = request.session.get('customer')
        customer = StripeCustomer.objects.filter(id=stripe_customer_id).first()
        billing_address_data = request.session.get('billing_address_data')
        billing_address_id = request.session.get('billing_address')
        vm_template_id = template.get('id', 1)

        # Make stripe charge to a customer
        stripe_utils = StripeUtils()
        card_details = stripe_utils.get_card_details(customer.stripe_id,
                                                     request.session.get(
                                                         'token'))
        if not card_details.get('response_object'):
            msg = card_details.get('error')
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='failed_payment')
            return HttpResponseRedirect(
                reverse('datacenterlight:payment') + '#payment_error')
        card_details_dict = card_details.get('response_object')
        cpu = specs.get('cpu')
        memory = specs.get('memory')
        disk_size = specs.get('disk_size')
        amount_to_be_charged = (cpu * 5) + (memory * 2) + (disk_size * 0.6)
        plan_name = "{cpu} Cores, {memory} GB RAM, {disk_size} GB SSD".format(
            cpu=cpu,
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
            customer.stripe_id,
            [{"plan": stripe_plan.get(
                'response_object').stripe_plan_id}])
        stripe_subscription_obj = subscription_result.get('response_object')
        # Check if the subscription was approved and is active
        if stripe_subscription_obj is None or \
                stripe_subscription_obj.status != 'active':
            msg = subscription_result.get('error')
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='failed_payment')
            return HttpResponseRedirect(
                reverse('datacenterlight:payment') + '#payment_error')
        create_vm_task.delay(vm_template_id, user, specs, template,
                             stripe_customer_id, billing_address_data,
                             billing_address_id,
                             stripe_subscription_obj, card_details_dict)
        request.session['order_confirmation'] = True
        return HttpResponseRedirect(reverse('datacenterlight:order_success'))

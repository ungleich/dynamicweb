from django.views.generic import FormView, CreateView, TemplateView, DetailView
from django.http import HttpResponseRedirect
from .forms import BetaAccessForm
from .models import BetaAccess, BetaAccessVMType, BetaAccessVM
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from django.core.mail import EmailMessage
from utils.mailer import BaseEmail
from django.shortcuts import render
from django.shortcuts import redirect
from django import forms
from django.core.exceptions import ValidationError
from django.views.decorators.cache import cache_control
from django.conf import settings
from utils.forms import BillingAddressForm, UserBillingAddressForm
from utils.models import BillingAddress
from membership.models import StripeCustomer
from hosting.models import HostingOrder, HostingBill
from utils.stripe_utils import StripeUtils
from datetime import datetime
from membership.models import CustomUser, StripeCustomer

from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineTemplateSerializer, VirtualMachineSerializer

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
            return HttpResponseRedirect(reverse('datacenterlight:order_confirmation'))            
        else:
            for session_var in ['specs', 'user', 'template', 'billing_address', 'billing_address_data', 'token', 'customer']:
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
                'templates': VirtualMachineTemplateSerializer(templates, many=True).data,
            }
        except:
            messages.error( request,
                'We have a temporary problem to connect to our backend. \
                Please try again in a few minutes'
                )
            context = {
                'error' : 'connection'
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

        request.session['template'] = VirtualMachineTemplateSerializer(template).data

        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')

        request.session['specs'] = {
            'cpu':cores,
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
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
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

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
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
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host()),
            'vms': vms
        })
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vms = BetaAccessVM.create(data)

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host()),
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

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return HttpResponseRedirect(self.get_success_url())


class IndexView(CreateView):
    template_name = "datacenterlight/index.html"
    model = BetaAccess
    form_class = BetaAccessForm
    success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"
    
    @cache_control(no_cache=True, must_revalidate=True, no_store=True)
    def get(self, request, *args, **kwargs):
        if 'specs' in request.session :
            del request.session['specs']
        if 'user' in request.session :
            del request.session['user']
        if 'billing_address_data' in request.session :
            del request.session['billing_address_data']
        try:
            manager = OpenNebulaManager()
            templates = manager.get_templates()
            context = {
                'templates': VirtualMachineTemplateSerializer(templates, many=True).data
            }
        except:
            messages.error( request,
                'We have a temporary problem to connect to our backend. \
                Please try again in a few minutes'
                )
            context = {
                'error' : 'connection'
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
        template_data = VirtualMachineTemplateSerializer(template).data
        
        name = request.POST.get('name')
        email = request.POST.get('email')
        name_field = forms.CharField()
        email_field = forms.EmailField()
        try:
            name = name_field.clean(name)
        except ValidationError as err:
            messages.add_message(self.request, messages.ERROR, '%(value) is not a proper name.'.format(name))
            return HttpResponseRedirect(reverse('datacenterlight:index'))

        try:    
            email = email_field.clean(email)
        except ValidationError as err:
            messages.add_message(self.request, messages.ERROR, '%(value) is not a proper email.'.format(email))
            return HttpResponseRedirect(reverse('datacenterlight:index'))

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
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        })
        return context

    def form_valid(self, form):

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
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

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(IndexView, self).form_valid(form)


class PaymentOrderView(FormView):
    template_name = 'hosting/payment.html'
    form_class = BillingAddressForm
    
    def get_form_kwargs(self):
        form_kwargs = super(PaymentOrderView, self).get_form_kwargs()
        billing_address_data = self.request.session.get('billing_address_data')
        if billing_address_data:
            form_kwargs.update({
                'initial': {
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
                custom_user = CustomUser.objects.get(email=user.get('email'))
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
                return self.render_to_response(self.get_context_data(form=form))

            # Create Billing Address
            billing_address = form.save()
            request.session['billing_address_data'] = billing_address_data
            request.session['billing_address'] = billing_address.id
            request.session['token'] = token
            request.session['customer'] = customer.id
            return HttpResponseRedirect(reverse('datacenterlight:order_confirmation'))
        else:
            return self.form_invalid(form)

class OrderConfirmationView(DetailView):
    template_name = "datacenterlight/order_detail.html"
    payment_template_name = 'hosting/payment.html'
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
        card_details = stripe_utils.get_card_details(customer.stripe_id, request.session.get('token'))
        context = {
            'site_url': reverse('datacenterlight:index'),
            'cc_last4' : card_details.get('response_object').get('last4'),
            'cc_brand' : card_details.get('response_object').get('brand')
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
        billing_address = BillingAddress.objects.filter(id=billing_address_id).first()
        token = request.session.get('token')
        vm_template_id = template.get('id', 1)
        final_price = specs.get('price')

        # Make stripe charge to a customer
        stripe_utils = StripeUtils()
        charge_response = stripe_utils.make_charge(amount=final_price,
                                                   customer=customer.stripe_id)
        charge = charge_response.get('response_object')

        # Check if the payment was approved
        if not charge:
            context.update({
                'paymentError': charge_response.get('error')
                # TODO add logic in payment form to autofill data 
                #'form': form
            })
            return render(request, self.payment_template_name, context)

        charge = charge_response.get('response_object')
        
        # Create OpenNebulaManager
        manager = OpenNebulaManager(email=settings.OPENNEBULA_USERNAME,
                                    password=settings.OPENNEBULA_PASSWORD)
        
        # Create a vm using oneadmin, also specify the name
        vm_id = manager.create_vm(
            template_id=vm_template_id,
            specs=specs,
            vm_name="{email}-{template_name}-{date}".format(
                   email=user.get('email'), 
                   template_name=template.get('name'),
                   date=int(datetime.now().strftime("%s")))
        )
        
        # Create a Hosting Order
        order = HostingOrder.create(
            price=final_price,
            vm_id=vm_id,
            customer=customer,
            billing_address=billing_address
        )
        
        # Create a Hosting Bill
        bill = HostingBill.create(
            customer=customer, billing_address=billing_address)

        # Create Billing Address for User if he does not have one
        if not customer.user.billing_addresses.count():
            billing_address_data.update({
                'user': customer.user.id
            })
            billing_address_user_form = UserBillingAddressForm(
                billing_address_data)
            billing_address_user_form.is_valid()
            billing_address_user_form.save()

        # Associate an order with a stripe payment
        order.set_stripe_charge(charge)

        # If the Stripe payment was successed, set order status approved
        order.set_approved()
        
        vm = VirtualMachineSerializer(manager.get_vm(vm_id)).data
        
        context = {
            'name': user.get('name'),
            'email': user.get('email'),
            'cores': specs.get('cpu'),
            'memory': specs.get('memory'),
            'storage': specs.get('disk_size'),
            'price': specs.get('price'),
            'template': template.get('name'),
            'vm.name': vm['name'],
            'vm.id': vm['vm_id'],
            'order.id': order.id
        }
        email_data = {
            'subject': settings.DCL_TEXT + " Order from %s" % context['email'],
            'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': ['info@ungleich.ch'],
            'body': "\n".join(["%s=%s" % (k, v) for (k, v) in context.items()]),
            'reply_to': [context['email']],
        }
        email = EmailMessage(**email_data)
        email.send()
        request.session['order_confirmation'] = True
        return HttpResponseRedirect(reverse('datacenterlight:order_success'))

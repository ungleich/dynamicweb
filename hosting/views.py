
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.views.generic import View, CreateView, FormView
from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings

from membership.forms import PaymentForm
from membership.models import CustomUser, StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.forms import BillingAddressForm
from utils.models import BillingAddress
from .models import VirtualMachineType, VirtualMachinePlan, HostingOrder
from .forms import HostingUserSignupForm, HostingUserLoginForm
from .mixins import ProcessVMSelectionMixin



class DjangoHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/django.html"

    def get_context_data(self, **kwargs):
        context = {
            'hosting': "django",
            'hosting_long': "Django",
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'email': "info@django-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)


class RailsHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/rails.html"

    def get_context_data(self, **kwargs):
        context = {
            'hosting': "rails",
            'hosting_long': "Ruby On Rails",
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class NodeJSHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/nodejs.html"

    def get_context_data(self, **kwargs):
        context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)


class IndexView(View):
    template_name = "hosting/index.html"

    def get_context_data(self, **kwargs):
        context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)


class LoginView(FormView):
    template_name = 'hosting/login.html'
    success_url = reverse_lazy('hosting:login')
    form_class = HostingUserLoginForm
    moodel = CustomUser

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth_user = authenticate(email=email, password=password)

        if auth_user:

            login(self.request, auth_user)
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())


class SignupView(CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    moodel = CustomUser

    def get_success_url(self):
        return reverse_lazy('hosting:signup')

    def form_valid(self, form):

        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        CustomUser.register(name, password, email)
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)

        return HttpResponseRedirect(self.get_success_url())


class PaymentVMView(FormView):
    template_name = 'hosting/payment.html'
    form_class = BillingAddressForm

    def get_context_data(self, **kwargs):
        context = super(PaymentVMView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            context = self.get_context_data()
            specifications = request.session.get('vm_specs')
            vm_type = specifications.get('hosting_company')
            vm = VirtualMachineType.objects.get(hosting_company=vm_type)
            final_price = vm.calculate_price(specifications)

            plan_data = {
                'vm_type': vm,
                'cores': specifications.get('cores'),
                'memory': specifications.get('memory'),
                'disk_size': specifications.get('disk_size'),
                'price': final_price
            }
            token = form.cleaned_data.get('token')

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=self.request.user.email,
                                                    token=token)
            # Create Virtual Machine Plan
            plan = VirtualMachinePlan.create(plan_data, request.user)

            # Create Billing Address
            billing_address = form.save()

            # Create a Hosting Order
            order = HostingOrder.create(VMPlan=plan, customer=customer,
                                        billing_address=billing_address)

            # Make stripe charge to a customer
            stripe_utils = StripeUtils()
            charge_response = stripe_utils.make_charge(amount=final_price,
                                              customer=customer.stripe_id)
            charge = charge_response.get('response_object')

            # Check if the payment was approved 
            if not charge:
                context.update({
                    'paymentError': charge_response.get('error'),
                    'form':form
                })
                return render(request, self.template_name, context)

            charge = charge_response.get('response_object')

            # Associate an order with a stripe payment
            order.set_stripe_charge(charge)

            # If the Stripe payment was successed, set order status approved
            order.set_approved()
            request.session.update({
                'charge':charge,
                'order':order.id,
                'billing_address':billing_address.id
            })
            return HttpResponseRedirect(reverse('hosting:invoice'))
        else:
            return self.form_invalid(form)

class InvoiceVMView(LoginRequiredMixin, View):
    template_name = "hosting/invoice.html"
    login_url = reverse_lazy('hosting:login')

    def get_context_data(self, **kwargs):
        charge = self.request.session.get('charge')
        order_id = self.request.session.get('order')
        billing_address_id = self.request.session.get('billing_address')
        last4 = charge.get('source').get('last4')
        brand = charge.get('source').get('brand')

        order = get_object_or_404(HostingOrder, pk=order_id)
        billing_address = get_object_or_404(BillingAddress, pk=billing_address_id)

        if not charge:
            return

        context = {
            'last4': last4,
            'brand': brand,
            'order': order,
            'billing_address': billing_address,
        }
        return context


    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)


class OrdersHostingView(LoginRequiredMixin, View):
    template_name = "hosting/orders.html"
    login_url = reverse_lazy('hosting:login')

    def get_context_data(self, **kwargs):
        user = self.request.user
        orders = HostingOrder.objects.filter(customer__user=user)
        context = {
            'orders':orders
        }

        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)



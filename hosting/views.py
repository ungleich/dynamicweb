
from django.shortcuts import get_object_or_404, render,render_to_response
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView, FormView, ListView, DetailView,\
    DeleteView, TemplateView, UpdateView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib import messages
from django.utils.encoding import force_bytes
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.conf import settings


from stored_messages.settings import stored_messages_settings
from stored_messages.models import Message
from stored_messages.api import mark_read


from membership.models import CustomUser, StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.forms import BillingAddressForm, PasswordResetRequestForm, SetPasswordForm
from utils.mailer import BaseEmail
from .models import VirtualMachineType, VirtualMachinePlan, HostingOrder
from .forms import HostingUserSignupForm, HostingUserLoginForm
from .mixins import ProcessVMSelectionMixin


class DjangoHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/django.html"

    def get_context_data(self, **kwargs):
        HOSTING = 'django'
        configuration_detail = dict(VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        context = {
            'hosting': HOSTING,
            'hosting_long': "Django",
            'configuration_detail': configuration_detail,
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'email': "info@django-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }

        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:djangohosting')
        context = self.get_context_data()

        return render(request, self.template_name, context)


class RailsHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/rails.html"

    def get_context_data(self, **kwargs):
        HOSTING = 'rails'
        configuration_detail = dict(VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        context = {
            'hosting': HOSTING,
            'configuration_detail': configuration_detail,
            'hosting_long': "Ruby On Rails",
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:railshosting')
        context = self.get_context_data()
        return render(request, self.template_name, context)


class NodeJSHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/nodejs.html"

    def get_context_data(self, **kwargs):
        HOSTING = 'nodejs'
        configuration_detail = dict(VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'configuration_detail': configuration_detail,
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:nodejshosting')
        context = self.get_context_data()

        return render(request, self.template_name, context)


class HostingPricingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/hosting_pricing.html"

    def get_context_data(self, **kwargs):
        configuration_options = dict(VirtualMachinePlan.VM_CONFIGURATION)
        context = {
            'configuration_options': configuration_options,
            'email': "info@django-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }

        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:djangohosting')
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
    success_url = reverse_lazy('hosting:orders')
    form_class = HostingUserLoginForm
    moodel = CustomUser

    def get_success_url(self):
        next_url = self.request.session.get('next', self.success_url)
        return next_url

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth_user = authenticate(email=email, password=password)

        if auth_user:
            login(self.request, auth_user)
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('hosting:notifications'))
        return super(LoginView, self).get(request, *args, **kwargs)


class SignupView(CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    model = CustomUser

    def get_success_url(self):
        next_url = self.request.session.get('next', reverse_lazy('hosting:signup'))
        return next_url

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        CustomUser.register(name, password, email)
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)

        return HttpResponseRedirect(self.get_success_url())


class PasswordResetView(FormView):
    template_name = 'hosting/reset_password.html'
    form_class = PasswordResetRequestForm
    success_message = "The link to reset your email has been sent to your email"
    success_url = reverse_lazy('hosting:login')
    # form_valid_message = 'Thank you for registering'

    def form_valid(self, form):

        email = form.cleaned_data.get('email')
        user = CustomUser.objects.get(email=email)

        messages.add_message(self.request, messages.SUCCESS, self.success_message)

        context = {
            'user': user,
            'token': default_token_generator.make_token(user),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'site_name': 'ungleich',
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())

        }
        email_data = {
            'subject': 'Password Reset',
            'to': email,
            'context': context,
            'template_name': 'password_reset_email',
            'template_path': 'emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        return HttpResponseRedirect(self.get_success_url())


class PasswordResetConfirmView(FormView):
    template_name = 'hosting/confirm_reset_password.html'
    form_class = SetPasswordForm
    success_url = reverse_lazy('hosting:login')

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        form = self.form_class(request.POST)

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')
                return self.form_valid(form)
            else:
                messages.error(request, 'Password reset has not been unsuccessful.')
                return self.form_invalid(form)

        else:
            messages.error(request, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


class NotificationsView(TemplateView):
    template_name = 'hosting/notifications.html'

    def get_context_data(self, **kwargs):
        context = super(NotificationsView, self).get_context_data(**kwargs)
        backend = stored_messages_settings.STORAGE_BACKEND()
        unread_notifications = backend.inbox_list(self.request.user)
        read_notifications = backend.archive_list(self.request.user)
        context.update({
            'unread_notifications': unread_notifications,
            'all_notifications': read_notifications + unread_notifications
        })
        return context


class MarkAsReadNotificationView(LoginRequiredMixin, UpdateView):
    model = Message
    success_url = reverse_lazy('hosting:notifications')
    fields = '__all__'

    def post(self, *args, **kwargs):
        message = self.get_object()
        backend = stored_messages_settings.STORAGE_BACKEND()
        backend.archive_store([self.request.user], message)
        mark_read(self.request.user, message)
        return HttpResponseRedirect(reverse('hosting:notifications'))


class GenerateVMSSHKeysView(LoginRequiredMixin, DetailView):
    model = VirtualMachinePlan
    template_name = 'hosting/virtual_machine_key.html'
    success_url = reverse_lazy('hosting:orders')
    context_object_name = "virtual_machine"

    def get_context_data(self, **kwargs):

        context = super(GenerateVMSSHKeysView, self).get_context_data(**kwargs)
        vm = self.get_object()
        if not vm.public_key:
            private_key = vm.generate_keys()
            context.update({
                'private_key': private_key
            })
            return context
        return context


class PaymentVMView(LoginRequiredMixin, FormView):
    template_name = 'hosting/payment.html'
    login_url = reverse_lazy('hosting:login')
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
                'configuration': specifications.get('configuration'),
                'price': final_price
            }
            token = form.cleaned_data.get('token')

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=self.request.user.email,
                                                    token=token)
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(self.get_context_data(form=form))

            # Create Virtual Machine Plan
            plan = VirtualMachinePlan.create(plan_data, request.user)

            # Create Billing Address
            billing_address = form.save()

            # Create a Hosting Order
            order = HostingOrder.create(vm_plan=plan, customer=customer,
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
                    'form': form
                })
                return render(request, self.template_name, context)

            charge = charge_response.get('response_object')

            # Associate an order with a stripe payment
            order.set_stripe_charge(charge)

            # If the Stripe payment was successed, set order status approved
            order.set_approved()

            # Send notification to ungleich as soon as VM has been booked
            # TODO send email using celery

            context = {
                'vm': plan,
                'order': order,
                'base_url': "{0}://{1}".format(request.scheme, request.get_host())

            }
            email_data = {
                'subject': 'New VM request',
                'to': request.user.email,
                'context': context,
                'template_name': 'new_booked_vm',
                'template_path': 'emails/'
            }
            email = BaseEmail(**email_data)
            email.send()

            return HttpResponseRedirect(reverse('hosting:orders', kwargs={'pk': order.id}))
        else:
            return self.form_invalid(form)


class OrdersHostingDetailView(LoginRequiredMixin, DetailView):
    template_name = "hosting/order_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('hosting:login')
    model = HostingOrder


class OrdersHostingListView(LoginRequiredMixin, ListView):
    template_name = "hosting/orders.html"
    login_url = reverse_lazy('hosting:login')
    context_object_name = "orders"
    model = HostingOrder
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        user = self.request.user
        self.queryset = HostingOrder.objects.filter(customer__user=user)
        return super(OrdersHostingListView, self).get_queryset()


class OrdersHostingDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('hosting:login')
    success_url = reverse_lazy('hosting:orders')
    model = HostingOrder


class VirtualMachinesPlanListView(LoginRequiredMixin, ListView):
    template_name = "hosting/virtual_machines.html"
    login_url = reverse_lazy('hosting:login')
    context_object_name = "vms"
    model = VirtualMachinePlan
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        user = self.request.user
        self.queryset = VirtualMachinePlan.objects.active(user)
        return super(VirtualMachinesPlanListView, self).get_queryset()


class VirtualMachineView(LoginRequiredMixin, UpdateView):
    template_name = "hosting/virtual_machine_detail.html"
    login_url = reverse_lazy('hosting:login')
    model = VirtualMachinePlan
    context_object_name = "virtual_machine"
    fields = '__all__'

    def get_success_url(self):
        vm = self.get_object()
        final_url = "%s%s" % (reverse('hosting:virtual_machines', kwargs={'pk': vm.id}),
                              '#status-v')
        return final_url

    def post(self, *args, **kwargs):
        vm = self.get_object()
        vm.cancel_plan()

        context = {
            'vm': vm,
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        }
        email_data = {
            'subject': 'Virtual machine plan canceled',
            'to': self.request.user.email,
            'context': context,
            'template_name': 'vm_status_changed',
            'template_path': 'emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        return HttpResponseRedirect(self.get_success_url())

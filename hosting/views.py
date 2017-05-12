from collections import namedtuple

from django.shortcuts import render
from django.http import Http404
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import View, CreateView, FormView, ListView, DetailView,\
    DeleteView, TemplateView, UpdateView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.conf import settings
from django.shortcuts import redirect


from guardian.mixins import PermissionRequiredMixin
from stored_messages.settings import stored_messages_settings
from stored_messages.models import Message
from stored_messages.api import mark_read


from membership.models import CustomUser, StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.forms import BillingAddressForm, PasswordResetRequestForm
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin, LoginViewMixin
from utils.mailer import BaseEmail
from .models import HostingOrder, HostingBill, UserHostingKey
from .forms import HostingUserSignupForm, HostingUserLoginForm, UserHostingKeyForm
from .mixins import ProcessVMSelectionMixin

from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineSerializer,\
                                       VirtualMachineTemplateSerializer

from oca.exceptions import OpenNebulaException
from oca.pool import WrongNameError


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
            'configuration_options': dict(VirtualMachinePlan.VM_CONFIGURATION)
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


class LoginView(LoginViewMixin):
    template_name = "hosting/login.html"
    form_class = HostingUserLoginForm
    success_url = reverse_lazy('hosting:orders')


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


class PasswordResetView(PasswordResetViewMixin):
    template_name = 'hosting/reset_password.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('hosting:login')
    template_email_path = 'hosting/emails/'


class PasswordResetConfirmView(PasswordResetConfirmViewMixin):
    template_name = 'hosting/confirm_reset_password.html'
    success_url = reverse_lazy('hosting:login')


class NotificationsView(LoginRequiredMixin, TemplateView):
    template_name = 'hosting/notifications.html'
    login_url = reverse_lazy('hosting:login')

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
    login_url = reverse_lazy('hosting:login')
    fields = '__all__'

    def post(self, *args, **kwargs):
        message = self.get_object()
        backend = stored_messages_settings.STORAGE_BACKEND()
        backend.archive_store([self.request.user], message)
        mark_read(self.request.user, message)
        return HttpResponseRedirect(reverse('hosting:notifications'))


class GenerateVMSSHKeysView(LoginRequiredMixin, FormView):
    form_class = UserHostingKeyForm
    model = UserHostingKey
    template_name = 'hosting/virtual_machine_key.html'
    success_url = reverse_lazy('hosting:orders')
    login_url = reverse_lazy('hosting:login')
    context_object_name = "virtual_machine"

    def get_context_data(self, **kwargs):
        try:
            user_key = UserHostingKey.objects.get(
                user=self.request.user
            )
        except UserHostingKey.DoesNotExist:
            user_key = None

        context = super(
            GenerateVMSSHKeysView,
            self
        ).get_context_data(**kwargs)

        context.update({
            'user_key': user_key
        })

        return context

    def get_form_kwargs(self):
        kwargs = super(GenerateVMSSHKeysView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.save()
        context = self.get_context_data()

        if form.cleaned_data.get('private_key'):
            context.update({
                'private_key': form.cleaned_data.get('private_key'),
                'key_name': form.cleaned_data.get('name')
            })

        # print("form", form.cleaned_data)

        return render(self.request, self.template_name, context)


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
            specifications = request.session.get('template')

            vm_template_id = specifications.get('id', 1)
            
            final_price = specifications.get('price', 1)

            token = form.cleaned_data.get('token')

            owner = self.request.user

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=owner.email,
                                                    token=token)
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(self.get_context_data(form=form))

            # Create Billing Address
            billing_address = form.save()

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

            # Create OpenNebulaManager 
            
            manager = OpenNebulaManager(email=owner.email,
                                        password=owner.password[0:20],
                                        create_user=True)
            template = manager.get_template(vm_template_id)

            # Create a vm using logged user
            vm_id = manager.create_vm(vm_template_id)
            # Create a Hosting Order
            order = HostingOrder.create(vm_id=vm_id, customer=customer,
                                        billing_address=billing_address)
            # Create a Hosting Bill
            bill = HostingBill.create(customer=customer, billing_address=billing_address)


            # Associate an order with a stripe payment
            order.set_stripe_charge(charge)

            # If the Stripe payment was successed, set order status approved
            order.set_approved()

            vm = VirtualMachineSerializer(manager.get_vm(vm_id)).data


            # Send notification to ungleich as soon as VM has been booked
            context = {
                'vm': vm,
                'order': order,
                'base_url': "{0}://{1}".format(request.scheme, request.get_host())

            }
            email_data = {
                'subject': 'New VM request',
                'to': request.user.email,
                'context': context,
                'template_name': 'new_booked_vm',
                'template_path': 'hosting/emails/'
            }
            email = BaseEmail(**email_data)
            email.send()

            return HttpResponseRedirect(reverse('hosting:orders', kwargs={'pk': order.id}))
        else:
            return self.form_invalid(form)


class OrdersHostingDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "hosting/order_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingorder']
    model = HostingOrder

    def get_context_data(self, **kwargs):
        # Get context
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password[0:20],
                                    create_user=True)
        vm = manager.get_vm(obj.vm_id)
        context['vm'] = VirtualMachineSerializer(vm).data


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
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password[0:20],
                                    create_user=True)
        queryset = manager.get_vms()
        serializer = VirtualMachineSerializer(queryset, many=True)
        return serializer.data


class CreateVirtualMachinesView(LoginRequiredMixin, View):
    template_name = "hosting/create_virtual_machine.html"
    login_url = reverse_lazy('hosting:login')

    def get(self, request, *args, **kwargs):
        #TODO: Replace with OpenNebulaManager.get_apps
        templates = OpenNebulaManager().get_templates()
        data = VirtualMachineTemplateSerializer(templates, many=True).data
        context = {
            'templates': data,
            #'configuration_options': VirtualMachinePlan.VM_CONFIGURATION
        }
        # context = {}
        return render(request, self.template_name, context)

    def post(self, request):
        #XXX: Fix this!
        #configuration = request.POST.get('configuration')
        #configuration_display = dict(VirtualMachinePlan.VM_CONFIGURATION).get(configuration)
        template_id = int(request.POST.get('vm_template_id'))
        template = OpenNebulaManager().get_template(template_id)
        data = VirtualMachineTemplateSerializer(template).data
        vm_specs = {
            #'configuration_display': configuration_display,
            #'configuration': configuration,
            'template': data, 
        }
        request.session['template'] = data 
        return redirect(reverse('hosting:payment'))


class VirtualMachineView(LoginRequiredMixin, View):
    template_name = "hosting/virtual_machine_detail.html"
    login_url = reverse_lazy('hosting:login')

    def get(self, request, *args, **kwargs):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password[0:20],
                                    create_user=True)
        vm_id = self.kwargs.get('pk')
        try:
            vm = manager.get_vm(vm_id)
            serializer = VirtualMachineSerializer(vm)
        except Exception as error:
            print(error)
            raise Http404()

        context = {
            'virtual_machine': serializer.data,
        }
        return render(request, self.template_name, context)

    def post(self, *args, **kwargs):
        #TODO: add api to OpenNebulaManager
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
            'template_path': 'hosting/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        return HttpResponseRedirect(self.get_success_url())

class HostingBillListView(LoginRequiredMixin, ListView):
    template_name = "hosting/bills.html"
    login_url = reverse_lazy('hosting:login')
    context_object_name = "users"
    model = StripeCustomer
    paginate_by = 10
    ordering = '-id'

class HostingBillDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "hosting/bill_detail.html"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingview']
    context_object_name = "bill"
    model = HostingBill

    def get_object(self, queryset=None):
        #Get HostingBill for primary key (Select from customer users)
        pk = self.kwargs['pk']
        object = HostingBill.objects.filter(customer__id=pk).first()
        if object is None:
            self.template_name = 'hosting/bill_error.html'
        return object

    def get_context_data(self, **kwargs):
        # Get context
        context = super(DetailView, self).get_context_data(**kwargs)

        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password[0:20],
                                    create_user=True)
        # Get vms
        queryset = manager.get_vms()
        vms = VirtualMachineSerializer(queryset, many=True).data
        context['vms'] = vms

        return context

from datetime import date
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
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator

from guardian.mixins import PermissionRequiredMixin
from stored_messages.settings import stored_messages_settings
from stored_messages.models import Message
from stored_messages.api import mark_read


from membership.models import CustomUser, StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.forms import BillingAddressForm, PasswordResetRequestForm, UserBillingAddressForm
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin, LoginViewMixin
from utils.mailer import BaseEmail
from .models import HostingOrder, HostingBill, HostingPlan, UserHostingKey
from .forms import HostingUserSignupForm, HostingUserLoginForm, UserHostingKeyForm
from .mixins import ProcessVMSelectionMixin

from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineSerializer,\
    VirtualMachineTemplateSerializer


from oca.exceptions import OpenNebulaException
from oca.pool import WrongNameError

CONNECTION_ERROR = "Your VMs cannot be displayed at the moment due to a backend \
                    connection error. please try again in a few minutes."


class DjangoHostingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/django.html"

    def get_context_data(self, **kwargs):
        HOSTING = 'django'
        templates = OpenNebulaManager().get_templates()
        data = VirtualMachineTemplateSerializer(templates, many=True).data
        configuration_options = HostingPlan.get_serialized_configs()

        # configuration_detail = dict(VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        context = {
            'hosting': HOSTING,
            'hosting_long': "Django",
            # 'configuration_detail': configuration_detail,
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'vm_types': data,
            'email': "info@django-hosting.ch",
            'configuration_options': configuration_options,
            'templates': templates,
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

        templates = OpenNebulaManager().get_templates()
        configuration_options = HostingPlan.get_serialized_configs()

        context = {
            'hosting': HOSTING,
            'hosting_long': "Ruby On Rails",
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            'configuration_options': configuration_options,
            'templates': templates,
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
        # configuration_detail = dict(VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        templates = OpenNebulaManager().get_templates()
        configuration_options = HostingPlan.get_serialized_configs()

        context = {
            'hosting': HOSTING,
            'hosting_long': "NodeJS",
            # 'configuration_detail': configuration_detail,
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'templates': templates,
            'configuration_options': configuration_options,

        }
        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:nodejshosting')
        context = self.get_context_data()

        return render(request, self.template_name, context)


class HostingPricingView(ProcessVMSelectionMixin, View):
    template_name = "hosting/hosting_pricing.html"

    def get_context_data(self, **kwargs):
        # configuration_options = dict(VirtualMachinePlan.VM_CONFIGURATION)
        templates = OpenNebulaManager().get_templates()
        configuration_options = HostingPlan.get_serialized_configs()

        context = {
            # 'configuration_options': configuration_options,
            'email': "info@django-hosting.ch",
            'templates': templates,
            'configuration_options': configuration_options,


        }

        return context

    def get(self, request, *args, **kwargs):
        request.session['hosting_url'] = reverse('hosting:djangohosting')
        context = self.get_context_data()

        return render(request, self.template_name, context)


class IndexView(View):
    template_name = "hosting/index.html"

    def get_context_data(self, **kwargs):
        templates = OpenNebulaManager().get_templates()
        data = VirtualMachineTemplateSerializer(templates, many=True).data

        context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': data
            # 'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }
        return context

    def get(self, request, *args, **kwargs):

        context = self.get_context_data()

        return render(request, self.template_name, context)


class LoginView(LoginViewMixin):
    template_name = "hosting/login.html"
    form_class = HostingUserLoginForm
    success_url = reverse_lazy('hosting:virtual_machines')


class SignupView(CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    model = CustomUser
    success_url = reverse_lazy('hosting:key_pair')

    def get_success_url(self):
        next_url = self.request.session.get(
            'next', self.success_url)
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

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)

            opennebula_client = OpenNebulaManager(
                email=user.email,
                password=user.password,
            )

        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None
            opennebula_client = None

        form = self.form_class(request.POST)

        if user is not None and default_token_generator.check_token(user, token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, 'Password has been reset.')

                # Change opennebula password
                opennebula_client.change_user_password(new_password)

                return self.form_valid(form)
            else:
                messages.error(
                    request, 'Password reset has not been successful.')
                form.add_error(None, 'Password reset has not been successful.')
                return self.form_invalid(form)

        else:
            messages.error(
                request, 'The reset password link is no longer valid.')
            form.add_error(None, 'The reset password link is no longer valid.')
            return self.form_invalid(form)


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
    login_url = reverse_lazy('hosting:login')
    context_object_name = "virtual_machine"

    def get_context_data(self, **kwargs):
        context = super(
            GenerateVMSSHKeysView,
            self
        ).get_context_data(**kwargs)

        try:
            user_key = UserHostingKey.objects.get(
                user=self.request.user
            )

        except UserHostingKey.DoesNotExist:
            user_key = None

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

        next_url = self.request.session.get(
            'next',
            reverse('hosting:create_virtual_machine')
        )

        if 'next' in self.request.session:
            context.update({
                'next_url': next_url
            })
            del (self.request.session['next'])

        if form.cleaned_data.get('private_key'):
            context.update({
                'private_key': form.cleaned_data.get('private_key'),
                'key_name': form.cleaned_data.get('name'),
                'form': UserHostingKeyForm(request=self.request),
            })

        owner = self.request.user
        # Create OpenNebulaManager
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # Get OpenNebula user id
        user_pool = manager._get_user_pool()
        opennebula_user = user_pool.get_by_name(owner.email)

        # Get user ssh key
        user_key = UserHostingKey.objects.get(user=owner)
        # Add ssh key to user
        manager.oneadmin_client.call('user.update', opennebula_user.id,
                                     '<CONTEXT><SSH_PUBLIC_KEY>{ssh_key}</SSH_PUBLIC_KEY></CONTEXT>'.format(ssh_key=user_key.public_key))

        return render(self.request, self.template_name, context)

    def post(self, request, *args, **kwargs):

        try:
            UserHostingKey.objects.get(
                user=self.request.user
            )
            return HttpResponseRedirect(reverse('hosting:key_pair'))

        except UserHostingKey.DoesNotExist:
            pass

        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class PaymentVMView(LoginRequiredMixin, FormView):
    template_name = 'hosting/payment.html'
    login_url = reverse_lazy('hosting:login')
    form_class = BillingAddressForm

    def get_form_kwargs(self):
        current_billing_address = self.request.user.billing_addresses.first()
        form_kwargs = super(PaymentVMView, self).get_form_kwargs()
        if not current_billing_address:
            return form_kwargs

        form_kwargs.update({
            'initial': {
                'street_address': current_billing_address.street_address,
                'city': current_billing_address.city,
                'postal_code': current_billing_address.postal_code,
                'country': current_billing_address.country,
            }
        })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(PaymentVMView, self).get_context_data(**kwargs)
        # Get user
        user = self.request.user

        # Get user last order
        last_hosting_order = HostingOrder.objects.filter(
            customer__user=user).last()

        # If user has already an hosting order, get the credit card data from
        # it
        if last_hosting_order:
            credit_card_data = last_hosting_order.get_cc_data()
            context.update({
                'credit_card_data': credit_card_data if credit_card_data else None,
            })

        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })

        return context

    def get(self, request, *args, **kwargs):
        try:
            UserHostingKey.objects.get(
                user=self.request.user
            )
        except UserHostingKey.DoesNotExist:
            messages.success(
                request,
                'In order to create a VM, you create/upload your SSH KEY first.'
            )
            return HttpResponseRedirect(reverse('hosting:key_pair'))

        if 'next' in request.session:
            del request.session['next']

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():

            # Get billing address data
            billing_address_data = form.cleaned_data

            context = self.get_context_data()

            template = request.session.get('template')
            specs = request.session.get('specs')

            vm_template_id = template.get('id', 1)

            final_price = specs.get('price')

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
                                        password=owner.password)
            # Get user ssh key
            try:
                user_key = UserHostingKey.objects.get(
                    user=self.request.user
                )

            except UserHostingKey.DoesNotExist:
                pass

            # Check if a bill for this customer in this month exits:
            today = date.today()
            month = today.month
            year = today.year

            try:
                bill = customer.hostingbill_set.all().filter(
                    date__year=year, date__month=month).order_by('-date').first()
            except IndexError:
                # Create a Hosting Bill
                bill = HostingBill.create(
                    customer=customer, billing_address=billing_address)

            # Create a Hosting Order
            order = HostingOrder.create(
                price=final_price,
                vm_id=0,
                customer=customer,
                billing_address=billing_address,
                bill=bill,
            )
            bill.total_price += final_price
            bill.save()

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

            # Create a vm using logged user
            vm_id = manager.create_vm(
                template_id=vm_template_id,
                specs=specs,
                ssh_key=user_key.public_key,
            )
            order.vm_id = vm_id
            order.save()
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
                                    password=owner.password)
        try:
            vm = manager.get_vm(obj.vm_id)
            context['vm'] = VirtualMachineSerializer(vm).data
        except ConnectionRefusedError:
            messages.error(request,
                           'In order to create a VM, you need to create/upload your SSH KEY first.'
                           )
        return context


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
                                    password=owner.password)
        try:
            queryset = manager.get_vms()
            serializer = VirtualMachineSerializer(queryset, many=True)
            return serializer.data
        except ConnectionRefusedError:
            messages.error(self.request,
                           'We could not load your VMs due to a backend connection \
                error. Please try again in a few minutes'
                           )

            self.kwargs['error'] = 'connection'
            return []

    def get_context_data(self, **kwargs):
        error = self.kwargs.get('error')
        if error is not None:
            print(error)
            context = {'error': 'connection'}
        else:
            context = super(ListView, self).get_context_data(**kwargs)
        return context


class CreateVirtualMachinesView(LoginRequiredMixin, View):
    template_name = "hosting/create_virtual_machine.html"
    login_url = reverse_lazy('hosting:login')

    def get(self, request, *args, **kwargs):

        try:
            UserHostingKey.objects.get(
                user=self.request.user
            )
        except UserHostingKey.DoesNotExist:
            messages.success(
                request,
                'In order to create a VM, you need to create/upload your SSH KEY first.'
            )
            return HttpResponseRedirect(reverse('hosting:key_pair'))

        try:
            manager = OpenNebulaManager()
            templates = manager.get_templates()
            configuration_options = HostingPlan.get_serialized_configs()

            context = {
                'templates': VirtualMachineTemplateSerializer(templates, many=True).data,
                'configuration_options': configuration_options,
            }
        except:
            messages.error(
                request,
                'We could not load the VM templates due to a backend connection \
                error. Please try again in a few minutes'
            )
            context = {
                'error': 'connection'
            }

        return render(request, self.template_name, context)

    def post(self, request):
        manager = OpenNebulaManager()
        template_id = request.POST.get('vm_template_id')
        template = manager.get_template(template_id)
        configuration_id = int(request.POST.get('configuration'))
        configuration = HostingPlan.objects.get(id=configuration_id)
        request.session['template'] = VirtualMachineTemplateSerializer(
            template).data

        request.session['specs'] = configuration.serialize()
        return redirect(reverse('hosting:payment'))


class VirtualMachineView(LoginRequiredMixin, View):
    template_name = "hosting/virtual_machine_detail.html"
    login_url = reverse_lazy('hosting:login')

    def get_object(self):
        owner = self.request.user
        vm = None
        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )
        vm_id = self.kwargs.get('pk')
        try:
            vm = manager.get_vm(vm_id)
            return vm
        except ConnectionRefusedError:
            messages.error(self.request,
                           'We could not load your VM due to a backend connection \
                error. Please try again in a few minutes'
                           )
            return None
        except Exception as error:
            print(error)
            raise Http404()

    def get_success_url(self):
        final_url = reverse('hosting:virtual_machines')
        return final_url

    def get(self, request, *args, **kwargs):
        vm = self.get_object()
        try:
            serializer = VirtualMachineSerializer(vm)
            context = {
                'virtual_machine': serializer.data,
            }
        except:
            pass

        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        owner = self.request.user
        vm = self.get_object()

        opennebula_vm_id = self.kwargs.get('pk')

        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )

        terminated = manager.delete_vm(
            vm.id
        )

        if not terminated:
            messages.error(
                request,
                'Error terminating VM %s' % (opennebula_vm_id)
            )
            return HttpResponseRedirect(self.get_success_url())

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

        messages.error(
            request,
            'VM %s terminated successfully' % (opennebula_vm_id)
        )

        return HttpResponseRedirect(self.get_success_url())


class HostingBillListView(LoginRequiredMixin, ListView):
    template_name = "hosting/bills.html"
    login_url = reverse_lazy('hosting:login')
    context_object_name = "bills"
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        user = self.request.user
        self.queryset = HostingBill.objects.filter(customer__user=user)
        return super(HostingBillListView, self).get_queryset()


class HostingBillDetailView(PermissionRequiredMixin, LoginRequiredMixin, DetailView):
    template_name = "hosting/bill_detail.html"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingbill']
    context_object_name = "bill"
    model = HostingBill

    def get_context_data(self, **kwargs):
        # Get context
        context = super(DetailView, self).get_context_data(**kwargs)

        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # Get vms
        vm_objs = []
        bill = context['bill']
        for order in bill.orders.all():
            vm = manager.get_vm(order.vm_id)
            vm_objs.append(vm)
        # Serialize vms
        vms = VirtualMachineSerializer(vm_objs, many=True).data

        # Set total price
        bill.total_price = 0.0
        for vm in vms:
            bill.total_price += vm['price']
        bill.save()
        context['vms'] = vms
        return context

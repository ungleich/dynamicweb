import json
import logging
import uuid

from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import Http404
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext_lazy as _
from django.views.generic import View, CreateView, FormView, ListView, \
    DetailView, \
    DeleteView, TemplateView, UpdateView
from guardian.mixins import PermissionRequiredMixin
from oca.pool import WrongIdError
from stored_messages.api import mark_read
from stored_messages.models import Message
from stored_messages.settings import stored_messages_settings

from datacenterlight.tasks import create_vm_task
from membership.models import CustomUser, StripeCustomer
from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineSerializer, \
    VirtualMachineTemplateSerializer
from utils.forms import BillingAddressForm, PasswordResetRequestForm, \
    UserBillingAddressForm
from utils.mailer import BaseEmail
from utils.stripe_utils import StripeUtils
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin, \
    LoginViewMixin
from .forms import HostingUserSignupForm, HostingUserLoginForm, \
    UserHostingKeyForm, generate_ssh_key_name
from .mixins import ProcessVMSelectionMixin
from .models import HostingOrder, HostingBill, HostingPlan, UserHostingKey

logger = logging.getLogger(__name__)

CONNECTION_ERROR = "Your VMs cannot be displayed at the moment due to a \
                    backend connection error. please try again in a few \
                    minutes."


class DashboardView(View):
    template_name = "hosting/dashboard.html"

    def get_context_data(self, **kwargs):
        context = {}
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


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
    success_url = reverse_lazy('hosting:dashboard')


class SignupView(CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    model = CustomUser
    success_url = reverse_lazy('hosting:ssh_keys')

    def get_success_url(self):
        next_url = self.request.session.get(
            'next', self.success_url)
        return next_url

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        this_base_url = "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host())
        CustomUser.register(name, password, email,
                            app='dcl', base_url=this_base_url)

        return HttpResponseRedirect(reverse_lazy('hosting:signup-validate'))


class SignupValidateView(TemplateView):
    template_name = "hosting/signup_validate.html"

    def get_context_data(self, **kwargs):
        context = super(SignupValidateView, self).get_context_data(**kwargs)
        login_url = '<a href="' + \
                    reverse('hosting:login') + '">' + str(_('login')) + '</a>'
        home_url = '<a href="' + \
                   reverse('datacenterlight:index') + '">Data Center Light</a>'
        message = '{signup_success_message} {lurl}</a> \
                 <br />{go_back} {hurl}.'.format(
            signup_success_message=_(
                'Thank you for signing up. We have sent an email to you. '
                'Please follow the instructions in it to activate your account. Once activated, you can login using'),
            go_back=_('Go back to'),
            lurl=login_url,
            hurl=home_url
        )
        context['message'] = mark_safe(message)
        context['section_title'] = _('Sign up')
        return context


class SignupValidatedView(SignupValidateView):
    template_name = "hosting/signup_validate.html"

    def get_context_data(self, **kwargs):
        context = super(SignupValidateView, self).get_context_data(**kwargs)
        validated = CustomUser.validate_url(self.kwargs['validate_slug'])
        login_url = '<a href="' + \
                    reverse('hosting:login') + '">' + str(_('login')) + '</a>'
        section_title = _('Account activation')
        if validated:
            message = '{account_activation_string} <br /> {login_string} {lurl}.'.format(
                account_activation_string=_(
                    "Your account has been activated."),
                login_string=_("You can now"),
                lurl=login_url)
        else:
            home_url = '<a href="' + \
                       reverse('datacenterlight:index') + \
                       '">Data Center Light</a>'
            message = '{sorry_message} <br />{go_back_to} {hurl}'.format(
                sorry_message=_("Sorry. Your request is invalid."),
                go_back_to=_('Go back to'),
                hurl=home_url
            )
        context['message'] = mark_safe(message)
        context['section_title'] = section_title
        return context


class PasswordResetView(PasswordResetViewMixin):
    site = 'dcl'
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

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, _('Password has been reset.'))

                # Change opennebula password
                opennebula_client.change_user_password(new_password)

                return self.form_valid(form)
            else:
                messages.error(
                    request, _('Password reset has not been successful.'))
                form.add_error(None,
                               _('Password reset has not been successful.'))
                return self.form_invalid(form)

        else:
            error_msg = _('The reset password link is no longer valid.')
            messages.error(request, _(error_msg))
            form.add_error(None, error_msg)
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


class SSHKeyDeleteView(LoginRequiredMixin, DeleteView):
    login_url = reverse_lazy('hosting:login')
    success_url = reverse_lazy('hosting:ssh_keys')
    model = UserHostingKey

    def get_object(self, queryset=None):
        """ Hook to ensure UserHostingKey object is owned by request.user.
            We reply with a Http404 if the user is not the owner of the key.
        """
        obj = super(SSHKeyDeleteView, self).get_object()
        if not obj.user == self.request.user:
            raise Http404
        return obj

    def delete(self, request, *args, **kwargs):
        owner = self.request.user
        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )
        pk = self.kwargs.get('pk')
        # Get user ssh key
        public_key = UserHostingKey.objects.get(pk=pk).public_key
        manager.manage_public_key([{'value': public_key, 'state': False}])

        return super(SSHKeyDeleteView, self).delete(request, *args, **kwargs)


class SSHKeyListView(LoginRequiredMixin, ListView):
    template_name = "hosting/user_keys.html"
    login_url = reverse_lazy('hosting:login')
    context_object_name = "keys"
    model = UserHostingKey
    paginate_by = 10
    ordering = '-id'

    def get_queryset(self):
        user = self.request.user
        self.queryset = UserHostingKey.objects.filter(user=user)
        return super(SSHKeyListView, self).get_queryset()

    def render_to_response(self, context, **response_kwargs):
        if not self.queryset:
            return HttpResponseRedirect(reverse('hosting:choice_ssh_keys'))
        return super(SSHKeyListView, self).render_to_response(context,
                                                              **response_kwargs)


class SSHKeyChoiceView(LoginRequiredMixin, View):
    template_name = "hosting/choice_ssh_keys.html"
    login_url = reverse_lazy('hosting:login')

    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    def post(self, request, *args, **kwargs):
        name = generate_ssh_key_name()
        private_key, public_key = UserHostingKey.generate_keys()
        content = ContentFile(private_key)
        ssh_key = UserHostingKey.objects.create(
            user=request.user, public_key=public_key, name=name)
        filename = name + '_' + str(uuid.uuid4())[:8] + '_private.pem'
        ssh_key.private_key.save(filename, content)
        owner = self.request.user
        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )
        public_key_str = public_key.decode()
        manager.manage_public_key([{'value': public_key_str, 'state': True}])
        return redirect(reverse_lazy('hosting:ssh_keys'), foo='bar')


class SSHKeyCreateView(LoginRequiredMixin, FormView):
    form_class = UserHostingKeyForm
    model = UserHostingKey
    template_name = 'hosting/user_key.html'
    login_url = reverse_lazy('hosting:login')
    context_object_name = "virtual_machine"
    success_url = reverse_lazy('hosting:ssh_keys')

    def get_form_kwargs(self):
        kwargs = super(SSHKeyCreateView, self).get_form_kwargs()
        kwargs.update({'request': self.request})
        return kwargs

    def form_valid(self, form):
        form.save()
        if 'dcl-generated-key-' in form.instance.name:
            content = ContentFile(form.cleaned_data.get('private_key'))
            filename = form.cleaned_data.get(
                'name') + '_' + str(uuid.uuid4())[:8] + '_private.pem'
            form.instance.private_key.save(filename, content)
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
        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )
        public_key = form.cleaned_data['public_key']
        if type(public_key) is bytes:
            public_key = public_key.decode()
        manager.manage_public_key([{'value': public_key, 'state': True}])
        return HttpResponseRedirect(self.success_url)

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        required = 'add_ssh' in self.request.POST
        form.fields['name'].required = required
        form.fields['public_key'].required = required
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)


class SettingsView(LoginRequiredMixin, FormView):
    template_name = "hosting/settings.html"
    login_url = reverse_lazy('hosting:login')
    form_class = BillingAddressForm

    def get_form(self, form_class):
        """
        Check if the user already saved contact details. If so, then show
        the form populated with those details, to let user change them.
        """
        return form_class(
            instance=self.request.user.billing_addresses.first(),
            **self.get_form_kwargs())

    def get_context_data(self, **kwargs):
        context = super(SettingsView, self).get_context_data(**kwargs)
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

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            billing_address_data = form.cleaned_data
            billing_address_data.update({
                'user': self.request.user.id
            })
            billing_address_user_form = UserBillingAddressForm(
                instance=self.request.user.billing_addresses.first(),
                data=billing_address_data)
            billing_address_user_form.save()
            return self.render_to_response(self.get_context_data())
        else:
            billing_address_data = form.cleaned_data
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
                'cardholder_name': current_billing_address.cardholder_name,
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
        if not UserHostingKey.objects.filter(user=self.request.user).exists():
            messages.success(
                request,
                'In order to create a VM, you create/upload your SSH KEY first.'
            )
            return HttpResponseRedirect(reverse('hosting:ssh_keys'))

        if 'next' in request.session:
            del request.session['next']

        return self.render_to_response(self.get_context_data())

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Get billing address data
            billing_address_data = form.cleaned_data
            token = form.cleaned_data.get('token')
            owner = self.request.user
            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=owner.email,
                                                    token=token)
            if not customer:
                msg = _("Invalid credit card")
                messages.add_message(
                    self.request, messages.ERROR, msg,
                    extra_tags='make_charge_error')
                return HttpResponseRedirect(
                    reverse('hosting:payment') + '#payment_error')

            # Create Billing Address
            billing_address = form.save()
            request.session['billing_address_data'] = billing_address_data
            request.session['billing_address'] = billing_address.id
            request.session['token'] = token
            request.session['customer'] = customer.id
            return HttpResponseRedirect("{url}?{query_params}".format(
                url=reverse('hosting:order-confirmation'),
                query_params='page=payment'))
        else:
            return self.form_invalid(form)


class OrdersHostingDetailView(LoginRequiredMixin,
                              DetailView):
    template_name = "hosting/order_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingorder']
    model = HostingOrder

    def get_object(self):
        return HostingOrder.objects.filter(
            pk=self.kwargs.get('pk')) if self.kwargs.get('pk') else None

    def get_context_data(self, **kwargs):
        # Get context
        context = super(DetailView, self).get_context_data(**kwargs)
        obj = self.get_object()
        owner = self.request.user
        stripe_customer_id = self.request.session.get('customer')
        customer = StripeCustomer.objects.filter(id=stripe_customer_id).first()
        stripe_utils = StripeUtils()
        card_details = stripe_utils.get_card_details(
            customer.stripe_id,
            self.request.session.get('token')
        )

        if self.request.GET.get('page') == 'payment':
            context['page_header_text'] = _('Confirm Order')
        else:
            context['page_header_text'] = _('Invoice')

        if obj is not None:
            try:
                manager = OpenNebulaManager(
                    email=owner.email, password=owner.password
                )
                vm = manager.get_vm(obj.vm_id)
                context['vm'] = VirtualMachineSerializer(vm).data
            except WrongIdError:
                messages.error(
                    self.request,
                    'The VM you are looking for is unavailable at the moment. \
                     Please contact Data Center Light support.'
                )
                self.kwargs['error'] = 'WrongIdError'
                context['error'] = 'WrongIdError'
            except ConnectionRefusedError:
                messages.error(
                    self.request,
                    'In order to create a VM, you need to create/upload your SSH KEY first.'
                )
        elif not card_details.get('response_object'):
            context['failed_payment'] = True
            context['card_details'] = card_details
        else:
            context['site_url'] = reverse('hosting:create_virtual_machine')
            context['cc_last4'] = card_details.get('response_object').get(
                'last4')
            context['cc_brand'] = card_details.get('response_object').get(
                'cc_brand')
            context['vm'] = self.request.session.get('specs')
        return context

    def get(self, request, *args, **kwargs):
        if 'specs' not in self.request.session:
            return HttpResponseRedirect(
                reverse('hosting:create_virtual_machine')
            )
        if 'token' not in self.request.session:
            return HttpResponseRedirect(reverse('hosting:payment'))
        self.object = self.get_object()
        context = self.get_context_data(object=self.object)
        if 'failed_payment' in context:
            msg = context['card_details'].get('error')
            messages.add_message(
                self.request, messages.ERROR, msg,
                extra_tags='failed_payment'
            )
            return HttpResponseRedirect(
                reverse('hosting:payment') + '#payment_error'
            )
        return self.render_to_response(context)

    def post(self, request):
        template = request.session.get('template')
        specs = request.session.get('specs')
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
        if stripe_subscription_obj is None or stripe_subscription_obj.status != 'active':
            msg = subscription_result.get('error')
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='failed_payment')
            return HttpResponseRedirect(
                reverse('hosting:payment') + '#payment_error')
        user = {
            'name': self.request.user.name,
            'email': self.request.user.email,
            'pass': self.request.user.password,
            'request_scheme': request.scheme,
            'request_host': request.get_host(),
            'language': get_language(),
        }
        create_vm_task.delay(vm_template_id, user, specs, template,
                             stripe_customer_id, billing_address_data,
                             billing_address_id,
                             stripe_subscription_obj, card_details_dict)

        for session_var in ['specs', 'template', 'billing_address',
                            'billing_address_data',
                            'token', 'customer']:
            if session_var in request.session:
                del request.session[session_var]

        response = {
            'status': True,
            'redirect': reverse('hosting:virtual_machines'),
            'msg_title': str(_('Thank you for the order.')),
            'msg_body': str(_('Your VM will be up and running in a few moments.'
                              ' We will send you a confirmation email as soon as'
                              ' it is ready.'))
        }

        return HttpResponse(json.dumps(response),
                            content_type="application/json")


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

        if not UserHostingKey.objects.filter(user=self.request.user).exists():
            messages.success(
                request,
                _(
                    'In order to create a VM, you need to create/upload your SSH KEY first.')
            )
            return HttpResponseRedirect(reverse('hosting:ssh_keys'))

        try:
            manager = OpenNebulaManager()
            templates = manager.get_templates()
            configuration_options = HostingPlan.get_serialized_configs()

            context = {
                'templates': VirtualMachineTemplateSerializer(templates,
                                                              many=True).data,
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
        except WrongIdError:
            messages.error(self.request,
                           _('We could not find the requested VM. Please \
                           contact Data Center Light Support.')
                           )
            return None
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
        if vm is None:
            return redirect(reverse('hosting:virtual_machines'))
        try:
            serializer = VirtualMachineSerializer(vm)
            context = {
                'virtual_machine': serializer.data,
                'order': HostingOrder.objects.get(
                    vm_id=serializer.data['vm_id'])
            }
        except Exception as ex:
            logger.debug("Exception generated {}".format(str(ex)))
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
        vm_data = VirtualMachineSerializer(manager.get_vm(vm.id)).data
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
            'vm': vm_data,
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host()),
            'page_header': _('Virtual Machine Cancellation')
        }
        email_data = {
            'subject': context['page_header'],
            'to': self.request.user.email,
            'context': context,
            'template_name': 'vm_canceled',
            'template_path': 'hosting/emails/',
            'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.error(
            request,
            _('VM %(VM_ID)s terminated successfully') % {
                'VM_ID': opennebula_vm_id}
        )

        return HttpResponseRedirect(self.get_success_url())


class HostingBillListView(PermissionRequiredMixin, LoginRequiredMixin,
                          ListView):
    template_name = "hosting/bills.html"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingview']
    context_object_name = "users"
    model = StripeCustomer
    paginate_by = 10
    ordering = '-id'


class HostingBillDetailView(PermissionRequiredMixin, LoginRequiredMixin,
                            DetailView):
    template_name = "hosting/bill_detail.html"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingview']
    context_object_name = "bill"
    model = HostingBill

    def get_object(self, queryset=None):
        # Get HostingBill for primary key (Select from customer users)
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
                                    password=owner.password)
        # Get vms
        queryset = manager.get_vms()
        vms = VirtualMachineSerializer(queryset, many=True).data
        # Set total price
        bill = context['bill']
        bill.total_price = 0.0
        for vm in vms:
            bill.total_price += vm['price']
        context['vms'] = vms
        return context

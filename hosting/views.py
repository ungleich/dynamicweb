import logging
import uuid
from datetime import datetime
from time import sleep

from django import forms
from django.conf import settings
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse_lazy, reverse
from django.http import (
    Http404, HttpResponseRedirect, HttpResponse, JsonResponse
)
from django.shortcuts import redirect, render
from django.utils.decorators import method_decorator
from django.utils.html import escape
from django.utils.http import urlsafe_base64_decode
from django.utils.safestring import mark_safe
from django.utils.translation import get_language, ugettext_lazy as _
from django.utils.translation import ugettext
from django.views.decorators.cache import never_cache
from django.views.generic import (
    View, CreateView, FormView, ListView, DetailView, DeleteView,
    TemplateView, UpdateView
)
from guardian.mixins import PermissionRequiredMixin
from oca.pool import WrongIdError
from stored_messages.api import mark_read
from stored_messages.models import Message
from stored_messages.settings import stored_messages_settings

from datacenterlight.models import VMTemplate, VMPricing
from datacenterlight.utils import create_vm, get_cms_integration
from hosting.models import UserCardDetail
from membership.models import CustomUser, StripeCustomer
from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import (
    VirtualMachineSerializer, VirtualMachineTemplateSerializer,
    VMTemplateSerializer
)
from utils.forms import (
    BillingAddressForm, PasswordResetRequestForm, UserBillingAddressForm,
    ResendActivationEmailForm
)
from utils.hosting_utils import get_vm_price_with_vat, HostingUtils
from utils.mailer import BaseEmail
from utils.stripe_utils import StripeUtils
from utils.tasks import send_plain_email_task
from utils.views import (
    PasswordResetViewMixin, PasswordResetConfirmViewMixin, LoginViewMixin,
    ResendActivationLinkViewMixin
)
from .forms import (
    HostingUserSignupForm, HostingUserLoginForm, UserHostingKeyForm,
    generate_ssh_key_name
)
from .mixins import ProcessVMSelectionMixin, HostingContextMixin
from .models import (
    HostingOrder, HostingBill, HostingPlan, UserHostingKey, VMDetail
)

logger = logging.getLogger(__name__)

CONNECTION_ERROR = "Your VMs cannot be displayed at the moment due to a \
                    backend connection error. please try again in a few \
                    minutes."
decorators = [never_cache]


class DashboardView(LoginRequiredMixin, View):
    template_name = "hosting/dashboard.html"
    login_url = reverse_lazy('hosting:login')

    def get_context_data(self, **kwargs):
        context = {}
        return context

    @method_decorator(decorators)
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

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class LoginView(HostingContextMixin, LoginViewMixin):
    template_name = "hosting/login.html"
    form_class = HostingUserLoginForm
    success_url = reverse_lazy('hosting:dashboard')


class SignupView(HostingContextMixin, CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    model = CustomUser
    success_url = reverse_lazy('hosting:dashboard')

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

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(self.get_success_url())
        return super(SignupView, self).get(request, *args, **kwargs)


class SignupValidateView(HostingContextMixin, TemplateView):
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
                'Please follow the instructions in it to activate your '
                'account. Once activated, you can login using'),
            go_back=_('Go back to'),
            lurl=login_url,
            hurl=home_url
        )
        context['message'] = mark_safe(message)
        context['section_title'] = _('Sign up')
        return context


class SignupValidatedView(SignupValidateView, HostingContextMixin):
    template_name = "hosting/signup_validate.html"

    def get_context_data(self, **kwargs):
        context = super(SignupValidateView, self).get_context_data(**kwargs)
        validated = CustomUser.validate_url(self.kwargs['validate_slug'])
        login_url = '<a href="' + \
                    reverse('hosting:login') + '">' + str(_('login')) + '</a>'
        section_title = _('Account activation')
        user = CustomUser.objects.filter(
            validation_slug=self.kwargs['validate_slug']).first()
        if validated:
            message = ('{account_activation_string} <br />'
                       ' {login_string} {lurl}.').format(
                account_activation_string=_(
                    "Your account has been activated."),
                login_string=_("You can now"),
                lurl=login_url)
            email_data = {
                'subject': _('Welcome to Data Center Light!'),
                'to': user.email,
                'context': {
                    'base_url': "{0}://{1}".format(
                        self.request.scheme,
                        self.request.get_host()
                    )
                },
                'template_name': 'welcome_user',
                'template_path': 'datacenterlight/emails/',
                'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
            }
            email = BaseEmail(**email_data)
            email.send()
        else:
            home_url = '<a href="' + \
                       reverse('datacenterlight:cms_index') + \
                       '">Data Center Light</a>'
            message = '{sorry_message} <br />{go_back_to} {hurl}'.format(
                sorry_message=_("Sorry. Your request is invalid."),
                go_back_to=_('Go back to'),
                hurl=home_url
            )
        context['message'] = mark_safe(message)
        context['section_title'] = section_title
        return context

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse_lazy('hosting:dashboard'))
        return super(SignupValidatedView, self).get(request, *args, **kwargs)


class ResendActivationEmailView(HostingContextMixin,
                                ResendActivationLinkViewMixin):
    template_name = 'hosting/resend_activation_link.html'
    form_class = ResendActivationEmailForm
    success_url = reverse_lazy('hosting:login')
    email_template_path = 'datacenterlight/emails/'
    email_template_name = 'user_activation'


class PasswordResetView(HostingContextMixin, PasswordResetViewMixin):
    site = 'dcl'
    template_name = 'hosting/reset_password.html'
    form_class = PasswordResetRequestForm
    success_url = reverse_lazy('hosting:login')
    template_email_path = 'hosting/emails/'


class PasswordResetConfirmView(HostingContextMixin,
                               PasswordResetConfirmViewMixin):
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
                opennebula_client.change_user_password(user.password)

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

    @method_decorator(decorators)
    def render_to_response(self, context, **response_kwargs):
        if not self.queryset:
            return HttpResponseRedirect(reverse('hosting:choice_ssh_keys'))
        return super(SSHKeyListView, self).render_to_response(context,
                                                              **response_kwargs)


class SSHKeyChoiceView(LoginRequiredMixin, View):
    template_name = "hosting/choice_ssh_keys.html"
    login_url = reverse_lazy('hosting:login')

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        context = {}
        return render(request, self.template_name, context)

    @method_decorator(decorators)
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


@method_decorator(decorators, name='dispatch')
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
        if settings.DCL_SSH_KEY_NAME_PREFIX in form.instance.name:
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


@method_decorator(decorators, name='dispatch')
class SettingsView(LoginRequiredMixin, FormView):
    template_name = "hosting/settings.html"
    login_url = reverse_lazy('hosting:login')
    form_class = BillingAddressForm
    permission_required = ['view_usercarddetail']

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
        stripe_customer = None
        if hasattr(user, 'stripecustomer'):
            stripe_customer = user.stripecustomer
        cards_list = UserCardDetail.get_all_cards_list(
            stripe_customer=stripe_customer
        )
        context.update({
            'cards_list': cards_list,
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })

        return context

    def post(self, request, *args, **kwargs):
        if 'card' in request.POST and request.POST['card'] is not '':
            card_id = escape(request.POST['card'])
            user_card_detail = UserCardDetail.objects.get(id=card_id)
            UserCardDetail.set_default_card(
                stripe_api_cus_id=request.user.stripecustomer.stripe_id,
                stripe_source_id=user_card_detail.card_id
            )
            msg = _(
                ("Your {brand} card ending in {last4} set as "
                 "default card").format(
                    brand=user_card_detail.brand,
                    last4=user_card_detail.last4
                )
            )
            messages.add_message(request, messages.SUCCESS, msg)
            return HttpResponseRedirect(reverse_lazy('hosting:settings'))
        if 'delete_card' in request.POST:
            try:
                card = UserCardDetail.objects.get(pk=self.kwargs.get('pk'))
                if (request.user.has_perm(self.permission_required[0], card)
                        and
                        request.user
                                .stripecustomer
                                .usercarddetail_set
                                .count() > 1):
                    if card.card_id is not None:
                        stripe_utils = StripeUtils()
                        stripe_utils.dissociate_customer_card(
                            request.user.stripecustomer.stripe_id,
                            card.card_id
                        )
                        if card.preferred:
                            UserCardDetail.set_default_card_from_stripe(
                                request.user.stripecustomer.stripe_id
                            )
                        card.delete()
                        msg = _("Card deassociation successful")
                        messages.add_message(request, messages.SUCCESS, msg)
                else:
                    msg = _("You are not permitted to do this operation")
                    messages.add_message(request, messages.ERROR, msg)
            except UserCardDetail.DoesNotExist:
                msg = _("The selected card does not exist")
                messages.add_message(request, messages.ERROR, msg)
            return HttpResponseRedirect(reverse_lazy('hosting:settings'))
        form = self.get_form()
        if form.is_valid():
            if 'billing-form' in request.POST:
                billing_address_data = form.cleaned_data
                billing_address_data.update({
                    'user': self.request.user.id
                })
                billing_address_user_form = UserBillingAddressForm(
                    instance=self.request.user.billing_addresses.first(),
                    data=billing_address_data)
                billing_address_user_form.save()
                msg = _("Billing address updated successfully")
                messages.add_message(request, messages.SUCCESS, msg)
            else:
                token = form.cleaned_data.get('token')
                stripe_utils = StripeUtils()
                card_details = stripe_utils.get_cards_details_from_token(
                    token
                )
                if not card_details.get('response_object'):
                    form.add_error("__all__", card_details.get('error'))
                    return self.render_to_response(self.get_context_data())
                stripe_customer = StripeCustomer.get_or_create(
                    email=request.user.email, token=token
                )
                card = card_details['response_object']
                if UserCardDetail.get_user_card_details(stripe_customer, card):
                    msg = _('You seem to have already added this card')
                    messages.add_message(request, messages.ERROR, msg)
                else:
                    acc_result = stripe_utils.associate_customer_card(
                        request.user.stripecustomer.stripe_id, token
                    )
                    if acc_result['response_object'] is None:
                        msg = _(
                            'An error occurred while associating the card.'
                            ' Details: {details}'.format(
                                details=acc_result['error']
                            )
                        )
                        messages.add_message(request, messages.ERROR, msg)
                        return self.render_to_response(self.get_context_data())
                    preferred = False
                    if stripe_customer.usercarddetail_set.count() == 0:
                        preferred = True
                    UserCardDetail.create(
                        stripe_customer=stripe_customer,
                        last4=card['last4'],
                        brand=card['brand'],
                        fingerprint=card['fingerprint'],
                        exp_month=card['exp_month'],
                        exp_year=card['exp_year'],
                        card_id=card['card_id'],
                        preferred=preferred
                    )
                    msg = _(
                        "Successfully associated the card with your account"
                    )
                    messages.add_message(request, messages.SUCCESS, msg)
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
        if hasattr(user, 'stripecustomer'):
            stripe_customer = user.stripecustomer
        else:
            stripe_customer = None
        cards_list = UserCardDetail.get_all_cards_list(
            stripe_customer=stripe_customer
        )
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY,
            'vm_pricing': VMPricing.get_vm_pricing_by_name(
                self.request.session.get('specs', {}).get('pricing_name')
            ),
            'cards_list': cards_list,
        })

        return context

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        if 'next' in request.session:
            del request.session['next']
        HostingUtils.clear_items_from_list(
            request.session,
            ['token', 'card_id', 'customer', 'user']
        )
        return self.render_to_response(self.get_context_data())

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            # Get billing address data
            billing_address_data = form.cleaned_data
            token = form.cleaned_data.get('token')
            owner = self.request.user
            if token is '':
                card_id = form.cleaned_data.get('card')
                customer = owner.stripecustomer
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
                        reverse('hosting:payment') + '#payment_error'
                    )
                request.session['card_id'] = user_card_detail.id
            else:
                # Get or create stripe customer
                customer = StripeCustomer.get_or_create(
                    email=owner.email, token=token
                )
                if not customer:
                    msg = _("Invalid credit card")
                    messages.add_message(
                        self.request, messages.ERROR, msg,
                        extra_tags='make_charge_error')
                    return HttpResponseRedirect(
                        reverse('hosting:payment') + '#payment_error')
                request.session['token'] = token
            request.session['billing_address_data'] = billing_address_data
            return HttpResponseRedirect("{url}?{query_params}".format(
                url=reverse('hosting:order-confirmation'),
                query_params='page=payment')
            )
        else:
            return self.form_invalid(form)


class OrdersHostingDetailView(LoginRequiredMixin, DetailView):
    template_name = "hosting/order_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('hosting:login')
    permission_required = ['view_hostingorder']
    model = HostingOrder

    def get_object(self, queryset=None):
        order_id = self.kwargs.get('pk')
        try:
            hosting_order_obj = HostingOrder.objects.get(pk=order_id)
            logger.debug("Found HostingOrder for id {order_id}".format(
                order_id=order_id
            ))
        except HostingOrder.DoesNotExist:
            logger.debug("HostingOrder not found for id {order_id}".format(
                order_id=order_id
            ))
            hosting_order_obj = None
        return hosting_order_obj

    def get_context_data(self, **kwargs):
        # Get context
        context = super(
            OrdersHostingDetailView, self
        ).get_context_data(**kwargs)
        obj = self.get_object()
        owner = self.request.user

        if self.request.GET.get('page') == 'payment':
            context['page_header_text'] = _('Confirm Order')
        else:
            context['page_header_text'] = _('Invoice')
            if not self.request.user.has_perm(
                    self.permission_required[0], obj
            ):
                logger.debug(
                    "User {user} does not have permission on HostingOrder "
                    "{order_id}. Raising 404 error now.".format(
                        user=self.request.user.email,
                        order_id=obj.id if obj else 'None'
                    )
                )
                raise Http404

        if obj is not None:
            # invoice for previous order
            try:
                vm_detail = VMDetail.objects.get(vm_id=obj.vm_id)
                context['vm'] = vm_detail.__dict__
                context['vm']['name'] = '{}-{}'.format(
                    context['vm']['configuration'], context['vm']['vm_id'])
                price, vat, vat_percent, discount = get_vm_price_with_vat(
                    cpu=context['vm']['cores'],
                    ssd_size=context['vm']['disk_size'],
                    memory=context['vm']['memory'],
                    pricing_name=(obj.vm_pricing.name
                                  if obj.vm_pricing else 'default')
                )
                context['vm']['vat'] = vat
                context['vm']['price'] = price
                context['vm']['discount'] = discount
                context['vm']['vat_percent'] = vat_percent
                context['vm']['total_price'] = price + vat - discount['amount']
                context['subscription_end_date'] = vm_detail.end_date()
            except VMDetail.DoesNotExist:
                try:
                    manager = OpenNebulaManager(
                        email=owner.email, password=owner.password
                    )
                    vm = manager.get_vm(obj.vm_id)
                    context['vm'] = VirtualMachineSerializer(vm).data
                    price, vat, vat_percent, discount = get_vm_price_with_vat(
                        cpu=context['vm']['cores'],
                        ssd_size=context['vm']['disk_size'],
                        memory=context['vm']['memory'],
                        pricing_name=(obj.vm_pricing.name
                                      if obj.vm_pricing else 'default')
                    )
                    context['vm']['vat'] = vat
                    context['vm']['price'] = price
                    context['vm']['discount'] = discount
                    context['vm']['vat_percent'] = vat_percent
                    context['vm']['total_price'] = (
                            price + vat - discount['amount']
                    )
                except WrongIdError:
                    messages.error(
                        self.request,
                        _('The VM you are looking for is unavailable at the '
                          'moment. Please contact Data Center Light support.')
                    )
                    self.kwargs['error'] = 'WrongIdError'
                    context['error'] = 'WrongIdError'
                except ConnectionRefusedError:
                    messages.error(
                        self.request,
                        _('In order to create a VM, you need to create/upload '
                          'your SSH KEY first.')
                    )
        else:
            # new order, confirm payment
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
            context['site_url'] = reverse('hosting:create_virtual_machine')
            context['vm'] = self.request.session.get('specs')
        return context

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        if not self.kwargs.get('pk'):
            if 'specs' not in self.request.session:
                return HttpResponseRedirect(
                    reverse('hosting:create_virtual_machine')
                )

            if ('token' not in self.request.session and
                    'card_id' not in self.request.session):
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

    @method_decorator(decorators)
    def post(self, request):
        template = request.session.get('template')
        specs = request.session.get('specs')
        stripe_utils = StripeUtils()
        # We assume that if the user is here, his/her StripeCustomer
        # object already exists
        stripe_customer_id = request.user.stripecustomer.id
        billing_address_data = request.session.get('billing_address_data')
        vm_template_id = template.get('id', 1)
        stripe_api_cus_id = request.user.stripecustomer.stripe_id
        if 'token' in self.request.session:
            card_details = stripe_utils.get_cards_details_from_token(
                request.session['token']
            )
            if not card_details.get('response_object'):
                return HttpResponseRedirect(reverse('hosting:payment'))
            card_details_response = card_details['response_object']
            card_details_dict = {
                'last4': card_details_response['last4'],
                'brand': card_details_response['brand'],
                'card_id': card_details_response['card_id']
            }
            ucd = UserCardDetail.get_user_card_details(
                request.user.stripecustomer, card_details_response
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
        if (stripe_subscription_obj is None or
                stripe_subscription_obj.status != 'active'):
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
                    url=reverse('hosting:payment'),
                    section='payment_error'),
                'msg_title': str(_('Error.')),
                'msg_body': str(
                    _('There was a payment related error.'
                      ' On close of this popup, you will be redirected back to'
                      ' the payment page.')
                )
            }
            return JsonResponse(response)

        if 'token' in request.session:
            ucd = UserCardDetail.get_or_create_user_card_detail(
                stripe_customer=self.request.user.stripecustomer,
                card_details=card_details_response
            )
            UserCardDetail.save_default_card_local(
                self.request.user.stripecustomer.stripe_id,
                ucd.card_id
            )
        user = {
            'name': self.request.user.name,
            'email': self.request.user.email,
            'pass': self.request.user.password,
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
            'redirect': reverse('hosting:virtual_machines'),
            'msg_title': str(_('Thank you for the order.')),
            'msg_body': str(
                _('Your VM will be up and running in a few moments.'
                  ' We will send you a confirmation email as soon as'
                  ' it is ready.'))
        }

        return JsonResponse(response)


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

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        return super(OrdersHostingListView, self).get(request, *args, **kwargs)


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
            if UserHostingKey.objects.filter(user=self.request.user).exists():
                context['show_create_ssh_key_msg'] = False
            else:
                context['show_create_ssh_key_msg'] = True
        return context


class CreateVirtualMachinesView(LoginRequiredMixin, View):
    template_name = "hosting/create_virtual_machine.html"
    login_url = reverse_lazy('hosting:login')

    def validate_cores(self, value):
        if (value > 48) or (value < 1):
            raise ValidationError(_('Invalid number of cores'))

    def validate_memory(self, value):
        if (value > 200) or (value < 1):
            raise ValidationError(_('Invalid RAM size'))

    def validate_storage(self, value):
        if (value > 2000) or (value < 10):
            raise ValidationError(_('Invalid storage size'))

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        context = {
            'templates': VMTemplate.objects.all(),
            'cms_integration': get_cms_integration('default'),
        }
        return render(request, self.template_name, context)

    @method_decorator(decorators)
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
            opennebula_vm_template_id=template_id).first()
        template_data = VMTemplateSerializer(template).data

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
            return redirect(CreateVirtualMachinesView.as_view())
        else:
            vm_pricing_name = vm_pricing.name

        try:
            cores = cores_field.clean(cores)
        except ValidationError as err:
            msg = '{} : {}.'.format(cores, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='cores')
            return redirect(CreateVirtualMachinesView.as_view())

        try:
            memory = memory_field.clean(memory)
        except ValidationError as err:
            msg = '{} : {}.'.format(memory, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='memory')
            return redirect(CreateVirtualMachinesView.as_view())

        try:
            storage = storage_field.clean(storage)
        except ValidationError as err:
            msg = '{} : {}.'.format(storage, str(err))
            messages.add_message(self.request, messages.ERROR, msg,
                                 extra_tags='storage')
            return redirect(CreateVirtualMachinesView.as_view())

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
            'discount': discount,
            'price': price,
            'vat': vat,
            'vat_percent': vat_percent,
            'total_price': price + vat - discount['amount'],
            'pricing_name': vm_pricing_name
        }

        request.session['specs'] = specs
        request.session['template'] = template_data
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
            logger.error(str(error))
            raise Http404()

    def get_success_url(self):
        final_url = reverse('hosting:virtual_machines')
        return final_url

    @method_decorator(decorators)
    def get(self, request, *args, **kwargs):
        vm = self.get_object()
        if vm is None:
            if self.request.is_ajax():
                storage = messages.get_messages(request)
                for m in storage:
                    pass
                storage.used = True
                return JsonResponse({'text': ugettext('Terminated')})
            else:
                return redirect(reverse('hosting:virtual_machines'))
        elif self.request.is_ajax():
            return HttpResponse()
        context = None
        try:
            serializer = VirtualMachineSerializer(vm)
            context = {
                'virtual_machine': serializer.data,
                'order': HostingOrder.objects.get(
                    vm_id=serializer.data['vm_id']
                )
            }
        except Exception as ex:
            logger.debug("Exception generated {}".format(str(ex)))
            messages.error(self.request,
                           _('We could not find the requested VM. Please '
                             'contact Data Center Light Support.')
                           )
            return redirect(reverse('hosting:virtual_machines'))

        return render(request, self.template_name, context)

    @method_decorator(decorators)
    def post(self, request, *args, **kwargs):
        response = {'status': False}
        admin_email_body = {}
        owner = self.request.user
        vm = self.get_object()

        manager = OpenNebulaManager(
            email=owner.email,
            password=owner.password
        )
        try:
            vm_data = VirtualMachineSerializer(manager.get_vm(vm.id)).data
            vm_name = vm_data.get('name')
        except WrongIdError as wrong_id_err:
            logger.error(str(wrong_id_err))
            return redirect(reverse('hosting:virtual_machines'))

        # Cancel Stripe subscription
        stripe_utils = StripeUtils()
        try:
            hosting_order = HostingOrder.objects.get(
                vm_id=vm.id
            )
            result = stripe_utils.unsubscribe_customer(
                subscription_id=hosting_order.subscription_id
            )
            stripe_subscription_obj = result.get('response_object')
            # Check if the subscription was canceled
            if (stripe_subscription_obj is None or
                    stripe_subscription_obj.status != 'canceled'):
                error_msg = result.get('error')
                logger.error(
                    'Error canceling subscription for {user} and vm id '
                    '{vm_id}'.format(user=owner.email, vm_id=vm.id)
                )
                logger.error(error_msg)
                admin_email_body['stripe_error_msg'] = error_msg
        except HostingOrder.DoesNotExist:
            error_msg = (
                "HostingOrder corresponding to vm_id={vm_id} does"
                "not exist. Hence, can not find subscription to "
                "cancel ".format(vm_id=vm.id)
            )
            logger.error(error_msg)
            admin_email_body['stripe_error_msg'] = error_msg

        terminated = manager.delete_vm(vm.id)

        if not terminated:
            logger.debug(
                "manager.delete_vm returned False. Hence, error making "
                "xml-rpc call to delete vm failed."
            )
            response['text'] = ugettext('Error terminating VM') + vm.id
        else:
            for t in range(15):
                try:
                    manager.get_vm(vm.id)
                except WrongIdError:
                    response['status'] = True
                    response['text'] = ugettext('Terminated')
                    vm_detail_obj = VMDetail.objects.filter(
                        vm_id=vm.id
                    ).first()
                    vm_detail_obj.terminated_at = datetime.utcnow()
                    vm_detail_obj.save()
                except BaseException as base_exception:
                    logger.error(
                        "manager.get_vm({vm_id}) returned exception: "
                        "{details}.".format(
                            details=str(base_exception), vm_id=vm.id
                        )
                    )
                    break
                else:
                    sleep(2)
            context = {
                'vm_name': vm_name,
                'base_url': "{0}://{1}".format(
                    self.request.scheme, self.request.get_host()
                ),
                'page_header': _('Virtual Machine %(vm_name)s Cancelled') % {
                    'vm_name': vm_name
                }
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
        admin_email_body.update(response)
        email_to_admin_data = {
            'subject': "Deleted VM and Subscription for VM {vm_id} and "
                       "user: {user}".format(
                           vm_id=vm.id, user=owner.email
                       ),
            'from_email': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': ['info@ungleich.ch'],
            'body': "\n".join(
                ["%s=%s" % (k, v) for (k, v) in admin_email_body.items()]),
        }
        send_plain_email_task.delay(email_to_admin_data)
        return JsonResponse(response)


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


def forbidden_view(request, exception=None, reason=''):
    """
    Handle 403 error
    """
    logger.error(str(exception) if exception else None)
    logger.error('Reason = {reason}'.format(reason=reason))
    err_msg = _('There was an error processing your request. Please try '
                'again.')
    messages.add_message(request, messages.ERROR, err_msg)
    return HttpResponseRedirect(request.get_full_path())

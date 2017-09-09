from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponseRedirect
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _
from django.views.generic import FormView, CreateView

from membership.models import CustomUser
from .forms import SetPasswordForm
from .mailer import BaseEmail


class SignupViewMixin(CreateView):
    model = CustomUser
    success_url = None

    def get_success_url(self):
        next_url = self.request.POST.get('next') if self.request.POST.get(
            'next') \
            else self.success_url

        return next_url

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        CustomUser.register(name, password, email)
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)

        return HttpResponseRedirect(self.get_success_url())


class LoginViewMixin(FormView):
    success_url = None

    def get_success_url(self):
        next_url = self.request.POST.get('next', self.success_url)
        if not next_url:
            return self.success_url
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
            return HttpResponseRedirect(self.get_success_url())

        return super(LoginViewMixin, self).get(request, *args, **kwargs)


class PasswordResetViewMixin(FormView):
    # template_name = 'hosting/reset_password.html'
    # form_class = PasswordResetRequestForm
    success_message = _(
        "The link to reset your email has been sent to your email")
    site = ''

    def test_generate_email_context(self, user):
        context = {
            'user': user,
            'token': default_token_generator.make_token(user),
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'site_name': 'ungleich' if self.site != 'dcl' else settings.DCL_TEXT,
            'base_url': "{0}://{1}".format(self.request.scheme,
                                           self.request.get_host())

        }
        return context

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        user = CustomUser.objects.get(email=email)
        messages.add_message(self.request, messages.SUCCESS,
                             self.success_message)
        context = self.test_generate_email_context(user)
        email_data = {
            'subject': _('Password Reset'),
            'to': email,
            'context': context,
            'template_name': 'password_reset_email',
            'template_path': self.template_email_path
        }
        if self.site == 'dcl':
            email_data['from_address'] = settings.DCL_SUPPORT_FROM_ADDRESS
        email = BaseEmail(**email_data)
        email.send()

        return HttpResponseRedirect(self.get_success_url())


class PasswordResetConfirmViewMixin(FormView):
    # template_name = 'hosting/confirm_reset_password.html'
    form_class = SetPasswordForm

    # success_url = reverse_lazy('hosting:login')

    def post(self, request, uidb64=None, token=None, *arg, **kwargs):
        try:
            uid = urlsafe_base64_decode(uidb64)
            user = CustomUser.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
            user = None

        form = self.form_class(request.POST)

        if user is not None and default_token_generator.check_token(user,
                                                                    token):
            if form.is_valid():
                new_password = form.cleaned_data['new_password2']
                user.set_password(new_password)
                user.save()
                messages.success(request, _('Password has been reset.'))
                return self.form_valid(form)
            else:
                messages.error(request,
                               _('Password reset has not been successful.'))
                form.add_error(None,
                               _('Password reset has not been successful.'))
                return self.form_invalid(form)

        else:
            messages.error(request,
                           _('The reset password link is no longer valid.'))
            form.add_error(None,
                           _('The reset password link is no longer valid.'))
            return self.form_invalid(form)

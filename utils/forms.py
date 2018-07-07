from django import forms
from django.contrib.auth import authenticate
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.translation import ugettext_lazy as _

from membership.models import CustomUser
from .models import ContactMessage, BillingAddress, UserBillingAddress


# from utils.fields import CountryField


class SignupFormMixin(forms.ModelForm):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(
                attrs={'placeholder': _('Enter your name or company name')}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password == password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password


class LoginFormMixin(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        fields = ['email', 'password']

    def clean(self):
        email = self.cleaned_data.get('email')
        password = self.cleaned_data.get('password')
        is_auth = authenticate(email=email, password=password)
        if not is_auth:
            raise forms.ValidationError(
                _("Your username and/or password were incorrect."))
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(_("User does not exist"))


class ResendActivationEmailForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            c = CustomUser.objects.get(email=email)
            if c.validated == 1:
                raise forms.ValidationError(
                    _("The account is already active."))
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(_("User does not exist"))


class PasswordResetRequestForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['email']

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError(_("User does not exist"))


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': _("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=_("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=_("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch', )
        return password2


class EditCreditCardForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())


class BillingAddressForm(forms.ModelForm):
    token = forms.CharField(widget=forms.HiddenInput(), required=False)
    card = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BillingAddress
        fields = ['cardholder_name', 'street_address',
                  'city', 'postal_code', 'country']
        labels = {
            'cardholder_name': _('Cardholder Name'),
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'Country': _('Country'),
        }


class BillingAddressFormSignup(BillingAddressForm):
    name = forms.CharField(label=_('Name'))
    email = forms.EmailField(label=_('Email Address'))
    field_order = ['name', 'email']

    class Meta:
        model = BillingAddress
        fields = ['name', 'email', 'cardholder_name', 'street_address',
                  'city', 'postal_code', 'country']
        labels = {
            'name': 'Name',
            'email': _('Email'),
            'cardholder_name': _('Cardholder Name'),
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'Country': _('Country'),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            raise forms.ValidationError(
                _("The email %(email)s is already registered with us. "
                  "Please reset your password and access your account.") %
                {'email': email}
            )
        except CustomUser.DoesNotExist:
            return email


class UserBillingAddressForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                  widget=forms.HiddenInput())

    class Meta:
        model = UserBillingAddress
        fields = ['cardholder_name', 'street_address',
                  'city', 'postal_code', 'country', 'user']
        labels = {
            'cardholder_name': _('Cardholder Name'),
            'street_address': _('Street Building'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'Country': _('Country'),
        }


class ContactUsForm(forms.ModelForm):
    error_css_class = 'autofocus'

    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'phone_number', 'message']
        widgets = {
            'name': forms.TextInput(attrs={'class': u'form-control'}),
            'email': forms.TextInput(attrs={'class': u'form-control'}),
            'phone_number': forms.TextInput(attrs={'class': u'form-control'}),
            'message': forms.Textarea(attrs={'class': u'form-control'}),
        }
        labels = {
            'name': _('Name'),
            'email': _('Email'),
            'phone_number': _('Phone number'),
            'message': _('Message'),
        }

    def send_email(self, email_to='info@digitalglarus.ch'):
        text_content = render_to_string(
            'emails/contact.txt', {'data': self.cleaned_data})
        html_content = render_to_string(
            'emails/contact.html', {'data': self.cleaned_data})
        email = EmailMultiAlternatives('Subject', text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [email_to]
        email.send()

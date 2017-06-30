from django import forms
from .models import ContactMessage, BillingAddress, UserBillingAddress
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import authenticate
from membership.models import CustomUser
# from utils.fields import CountryField


class SignupFormMixin(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': _('Enter your name or company name')}),
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
            raise forms.ValidationError("Your username and/or password were incorrect.")
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data.get('email')
        try:
            CustomUser.objects.get(email=email)
            return email
        except CustomUser.DoesNotExist:
            raise forms.ValidationError("User does not exist")
        else:
            return email


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
            raise forms.ValidationError("User does not exist")
        else:
            return email


class SetPasswordForm(forms.Form):
    """
    A form that lets a user change set their password without entering the old
    password
    """
    error_messages = {
        'password_mismatch': ("The two password fields didn't match."),
    }
    new_password1 = forms.CharField(label=("New password"),
                                    widget=forms.PasswordInput)
    new_password2 = forms.CharField(label=("New password confirmation"),
                                    widget=forms.PasswordInput)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError(
                    self.error_messages['password_mismatch'],
                    code='password_mismatch',)
        return password2


class EditCreditCardForm(forms.Form):
    token = forms.CharField(widget=forms.HiddenInput())


class BillingAddressForm(forms.ModelForm):
    token = forms.CharField(widget=forms.HiddenInput(), required=False)

    class Meta:
        model = BillingAddress
        fields = ['street_address', 'city', 'postal_code', 'country']
        labels = {
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'Country': _('Country'),
        }


class UserBillingAddressForm(forms.ModelForm):
    user = forms.ModelChoiceField(queryset=CustomUser.objects.all(),
                                  widget=forms.HiddenInput())

    class Meta:
        model = UserBillingAddress
        fields = ['street_address', 'city', 'postal_code', 'country', 'user']
        labels = {
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
        text_content = render_to_string('emails/contact.txt', {'data': self.cleaned_data})
        html_content = render_to_string('emails/contact.html', {'data': self.cleaned_data})
        email = EmailMultiAlternatives('Subject', text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [email_to]
        email.send()

from django import forms
from django.utils.translation import ugettext_lazy as _


from utils.models import BillingAddress
from utils.forms import LoginFormMixin, SignupFormMixin, BillingAddressForm

from .models import MembershipType


class LoginForm(LoginFormMixin):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(SignupFormMixin):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())
    name = forms.CharField(label='name',
                           widget=forms.TextInput(attrs={'placeholder': 'Full name'}))


class MembershipBillingForm(BillingAddressForm):
    token = forms.CharField(widget=forms.HiddenInput())
    membership_type = forms.ModelChoiceField(queryset=MembershipType.objects.all(),
                                             widget=forms.HiddenInput())

    class Meta:
        model = BillingAddress
        fields = ['membership_type', 'street_address', 'city', 'postal_code', 'country']
        labels = {
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'country': _('Country'),
        }

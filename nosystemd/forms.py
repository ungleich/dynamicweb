from django import forms
from django.utils.translation import ugettext_lazy as _


from utils.forms import LoginFormMixin, SignupFormMixin, BillingAddressForm
from utils.models import BillingAddress

from .models import Donation, DonatorStatus


class LoginForm(LoginFormMixin):
    email = forms.CharField(widget=forms.EmailInput())
    password = forms.CharField(widget=forms.PasswordInput())


class SignupForm(SignupFormMixin):
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())


class DonationForm(forms.ModelForm):

    class Meta:
        model = Donation
        fields = ['donation', 'donator', 'billing_address',
                  'last4', 'cc_brand', 'stripe_charge_id']

    def save(self, commit=True):
        instance = super(DonationForm, self).save(commit=False)

        if commit:
            DonatorStatus.create(self.cleaned_data['donator'].user)
            instance.save()

        return instance


class DonationBillingForm(BillingAddressForm):
    token = forms.CharField(widget=forms.HiddenInput())
    donation_amount = forms.FloatField(widget=forms.TextInput(attrs={'placeholder': 'Amount'}))

    class Meta:
        model = BillingAddress
        fields = ['donation_amount', 'street_address', 'city', 'postal_code', 'country']
        labels = {
            'amount': _('Amount'),
            'street_address': _('Street Address'),
            'city': _('City'),
            'postal_code': _('Postal Code'),
            'Country': _('Country'),
        }

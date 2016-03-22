__author__ = 'tomislav'
from django import forms
from django.utils.translation import ugettext_lazy as _
import six

from .models import CreditCards


class LoginForm(forms.Form):
    email = forms.EmailField(label="Email address", max_length=50,
                             widget=forms.TextInput(
                                 attrs={'class': 'form-control', 'placeholder': 'Enter email'}))
    password = forms.CharField(label='Password', max_length=50,
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control', 'placeholder': 'Password',
                                          'type': 'password'}))


class RegisterForm(LoginForm):
    name = forms.CharField(label='Name', max_length=50,
                           widget=forms.TextInput(
                               attrs={'class': 'form-control', 'placeholder': 'Enter name'}))


class PaymentForm(forms.ModelForm):
    class Meta:
        model = CreditCards
        fields = ('name', 'card_number', 'expiry_date', 'ccv', 'user_id')
        labels = {'name': _('Name'), 'card_number': _('Card number'), 'expiry_date': _('Expiry date'),
                  'ccv': _('CCV')}
        exclude = ('user_id','payment_type')
        widgets = {
            'name': forms.TextInput(
                attrs={'class': 'form-control', "placeholder": "Enter name on card",
                       'placeholder': 'Enter name on card'}),
            'card_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Card Number','data-stripe':'number'}),
            'expiry_date': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'MM/YYYY'}),
            'ccv': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'CCV','data-stripe':'cvc'})}

    def clean(self):
        data = self.cleaned_data

        # if CreditCards.objects.filter(card_number=data.get("card_number")):
        #     raise forms.ValidationError({'card_number': _('Credit card is used before.')})
        return self.cleaned_data

    def save(self, user_id):
        self.instance.user_id = user_id
        self.instance.user_id_id = user_id.id
        super(PaymentForm, self).save()

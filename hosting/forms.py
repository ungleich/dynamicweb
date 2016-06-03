from django import forms
from membership.models import CustomUser
from django.contrib.auth import authenticate

from utils.stripe_utils import StripeUtils

from .models import HostingOrder


class HostingOrderAdminForm(forms.ModelForm):

    class Meta:
        model = HostingOrder
        fields = ['vm_plan', 'customer']

    def clean(self):
        customer = self.cleaned_data.get('customer')
        vm_plan = self.cleaned_data.get('vm_plan')

        # Make a charge to the customer
        stripe_utils = StripeUtils()
        charge_response = stripe_utils.make_charge(customer=customer.stripe_id,
                                                   amount=vm_plan.price)
        charge = charge_response.get('response_object')
        if not charge:
            raise forms.ValidationError(charge_response.get('error'))

        self.cleaned_data.update({
            'charge': charge
        })
        return self.cleaned_data


class HostingUserLoginForm(forms.Form):

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
            raise forms.ValidationError("User does not exists")
        else:
            return email


class HostingUserSignupForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput())
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = CustomUser
        fields = ['name', 'email', 'password']
        widgets = {
            'name': forms.TextInput(attrs={'placeholder': 'Enter your name or company name'}),
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not confirm_password == password:
            raise forms.ValidationError("Passwords don't match")
        return confirm_password

from django import forms

from .models import BetaAccess, ContactUs


class BetaAccessForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['name', 'email']
        model = BetaAccess


class ContactForm(forms.ModelForm):

    class Meta:
        fields = ['name', 'email', 'message']
        model = ContactUs


# class BetaAccessVMForm(forms.ModelForm):
#     type = forms.CharField(widget=forms.EmailInput())

#     class Meta:
#         fields = ['email']
#         model = BetaAccessVM

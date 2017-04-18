from django import forms

from .models import BetaAccess, BetaAccessVM


class BetaAccessForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['email']
        model = BetaAccess


# class BetaAccessVMForm(forms.ModelForm):
#     type = forms.CharField(widget=forms.EmailInput())

#     class Meta:
#         fields = ['email']
#         model = BetaAccessVM

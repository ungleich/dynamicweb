from django import forms

from .models import BetaAccess


class BetaAccessForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['name', 'email']
        model = BetaAccess


# class BetaAccessVMForm(forms.ModelForm):
#     type = forms.CharField(widget=forms.EmailInput())

#     class Meta:
#         fields = ['email']
#         model = BetaAccessVM

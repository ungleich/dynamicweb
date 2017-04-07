from django import forms

from .models import BetaAccess


class BetaAccessForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput())

    class Meta:
        fields = ['email']
        model = BetaAccess

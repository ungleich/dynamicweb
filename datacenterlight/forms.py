from django import forms

from .models import ContactUs


class ContactForm(forms.ModelForm):
    class Meta:
        fields = ['name', 'email', 'message']
        model = ContactUs

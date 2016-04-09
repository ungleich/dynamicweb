from django import forms
from .models import Message
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.translation import ugettext_lazy as _


class ContactUsForm(forms.ModelForm):
    error_css_class = 'autofocus'

    class Meta:
        model = Message
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

    def send_email(self):
        text_content = render_to_string('emails/contact.txt', {'data': self.cleaned_data})
        html_content = render_to_string('emails/contact.html', {'data': self.cleaned_data})
        email = EmailMultiAlternatives('Subject', text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = ['info@digitalglarus.ch']
        email.send()

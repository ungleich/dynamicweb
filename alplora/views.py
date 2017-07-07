from django.views.generic import TemplateView

from django.utils.translation import get_language, get_language_info
from django.utils.translation import ugettext_lazy as _
from django.views.generic.edit import FormView
from django.contrib import messages
from django.shortcuts import render

from utils.forms import ContactUsForm


class IndexView(TemplateView):
    template_name = "alplora/index.html"

    def get_context_data(self, *args, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        languages = getlanguages()
        context.update(languages)
        return context


class ContactView(FormView):
    template_name = 'alplora/contact.html'
    form_class = ContactUsForm
    success_message = _('Message Successfully Sent')

    def get_context_data(self, *args, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        languages = getlanguages()
        context.update(languages)
        return context

    def form_valid(self, form):
        form.save()
        form.send_email(email_to='info@alplora.ch')
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return render(self.request, 'alplora/contact_success.html', {})


class LoginView(TemplateView):
    template_name = "alplora/login.html"

    def get_context_data(self, *args, **kwargs):
        context = super(LoginView, self).get_context_data(**kwargs)
        languages = getlanguages()
        context.update(languages)
        return context


def getlanguages():
    language = get_language()
    language_activate = get_language_info(language)
    if language == 'de':
        list_language = {
            'name': 'English',
            'code': 'en-us'
        }
    else:
        list_language = {
            'name': 'Deutsch',
            'code': 'de'
        }

    return {
        'language': language,
        'list_language': list_language,
        'language_activate': language_activate['name_local']
    }

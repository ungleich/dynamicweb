from django.contrib import messages

from django.views.generic.edit import FormView
from django.utils.translation import ugettext_lazy as _
from django.core.urlresolvers import reverse_lazy
from django.views.generic import View
from django.shortcuts import render

from utils.forms import ContactUsForm


class LandingView(View):
    template_name = "ungleich_page/landing.html"
    form_class = ContactUsForm

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})


class ContactView(FormView):
    template_name = 'ungleich_page/landing.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('ungleich_page:landing')
    success_message = _('Message Successfully Sent')

    def form_valid(self, form):
        form.save()
        form.send_email()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(ContactView, self).form_valid(form)

    def get_context_data(self, **kwargs):
        context = super(ContactView, self).get_context_data(**kwargs)
        context['page_title'] = _('Contact Us')
        context['page_subtitle'] = _('If you have any question, just send us an email.')
        return context

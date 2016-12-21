from django.views.generic import FormView, CreateView
from .forms import BetaAccessForm
from .models import BetaAccess
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse


class IndexView(CreateView):
    template_name = "datacenterlight/index.html"
    model = BetaAccess
    form_class = BetaAccessForm
    success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def get_success_url(self):
        success_url = reverse('datacenterlight:index')
        success_url += "#requestform"
        return success_url

    def form_valid(self, form):
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(IndexView, self).form_valid(form)

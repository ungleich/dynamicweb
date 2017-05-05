from django.shortcuts import get_object_or_404, render
from django.views import generic

from .models import Bill


class IndexView(generic.ListView):
    template_name = 'bill/index.html'
    context_object_name = 'latest_bill_list'

    def get_queryset(self):
        # Return the latest five bills
        return Bill.objects.order_by('-date')[:5]


class DetailView(generic.DetailView):
    model = Bill
    template_name = 'bill/detail.html'

    def get_context_data(self, **kwargs):
        context = super(DetailView, self).get_context_data(**kwargs)
        context['bill'].prepare()
        return context

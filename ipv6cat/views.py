import ipaddress
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib import messages
from django.views.generic import DetailView
from .forms import CatCreateForm
from .models import Cat

# Create your views here.
def get_ip(request):
    try:
        x_forward = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forward:
            ip = x_forward.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
    except:
        ip=""
    return ip


def home(request):
    client_ip = get_ip(request)
    if ipaddress.ip_address(client_ip).__class__ is ipaddress.IPv4Address:
        messages.success(request, 'You are great!')
        ip_valid = True
    else:
        messages.error(request, 'Oh, sorry...')
        ip_valid = False
    cats = Cat.objects.all()
    if request.method == 'POST':
        form = CatCreateForm(request.POST or None, request.FILES or None)
        if form.is_valid():
            cd = form.cleaned_data
            new_cat = form.save(commit = False)
            new_cat.save()
            return redirect(new_cat.get_absolute_url())
    else:
        form = CatCreateForm()
    return render(request, 'ipv6cat/welcome.html', {'form': form, 'ip_valid': ip_valid, 'cats': cats})


class CatDetailView(DetailView):
    def get_queryset(self):
        return Cat.objects.all()
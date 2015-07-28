import datetime

from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from .models import RailsBetaUser

class RailsBetaUserForm(ModelForm):
    required_css_class = 'form-control'
    class Meta:
        model = RailsBetaUser
        fields = [ 'email' ]

def index(request):
    email = RailsBetaUser(received_date=datetime.datetime.now())
    context = {}
    context['form'] = RailsBetaUserForm()

    if request.method == 'POST':
        form = RailsBetaUserForm(request.POST, instance=email)
        context['form'] = form
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("railshosting:beta"))
        else:
            context['error_message'] = "a problem"

    return render(request, 'railshosting/index.html', context)

def djangohosting(request):
    return render(request, 'railshosting/django.html')

def beta(request):
    return render(request, 'railshosting/beta.html')

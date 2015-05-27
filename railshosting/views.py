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
    form = RailsBetaUserForm()
    return render(request, 'railshosting/index.html')

def beta(request):
    message = RailsBetaUser(received_date=datetime.datetime.now())
    form = MessageForm(request.POST, instance=message)

    context = { 
        'email': form,
    }

    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("railshosting:beta")

    return render(request, 'railshosting/beta.html', context)

import datetime

from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse

from django.core.mail import send_mail

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
            email = form.cleaned_data['email']
            send_mail('(Rails-)Hosting request', "email: %s" % email, 'django@ungleich.ch', ['nico.schottelius@ungleich.ch'], fail_silently=False)
            # mail_managers(subject, message, fail_silently=False, connection=None, html_message=None)[source]
            return HttpResponseRedirect(reverse("railshosting:beta"))
        else:
            context['error_message'] = "a problem"

    return render(request, 'railshosting/index.html', context)

def hosting(request, context, page):
    email = RailsBetaUser(received_date=datetime.datetime.now())

    if request.method == 'POST':
        context['form'] = RailsBetaUserForm(request.POST, instance=email)
        if context['form'].is_valid():
            context['form'].save()
            email = context['form'].cleaned_data['email']
            subject = "%shosting request" % context['hosting']
            message = "Request for beta by: %s" % email

            mail_managers(subject, message)

            return HttpResponseRedirect(reverse("railshosting:beta"))
        else:
            context['form'] = RailsBetaUserForm()
            context['error_message'] = "a problem"

    page = "railshosting/%s.html" % page

    return render(request, page, context)

################################################################################
# Hostings
#
def djangohosting(request):
    context = {}
    context["hosting"]="django"
    context["hosting_long"]="Django"
    context["domain"]="django-hosting.ch"
    context["google_analytics"]="the right id"
    context["email"]="info@django-hosting.ch"

    return hosting(request, context["hosting"], context)

def railshosting(request):
    context = {}
    context["hosting"]="rails"
    context["hosting_long"]="Ruby On Rails"
    context["domain"]="rails-hosting.ch"
    context["google_analytics"]="the right id"
    context["email"]="info@rails-hosting.ch"

    return hosting(request, context["hosting"], context)

def nodejshosting(request):
    context = {}

    context["hosting"]="nodejs"
    context["hosting_long"]="NodeJS"
    context["domain"]="node-hosting.ch"
    context["google_analytics"]="the right id"
    context["email"]="info@node-hosting.ch"
    
    return hosting(request, context["hosting"], context)

def beta(request):
    return render(request, 'railshosting/beta.html')


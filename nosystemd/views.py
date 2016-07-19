from django.shortcuts import render
from django.views.generic import TemplateView, FormView
from .forms import LoginForm

# Create your views here.


class LandingView(TemplateView):
    template_name = "nosystemd/landing.html"

class LoginView(FormView):
    template_name = "nosystemd/login.html"
    form_class = LoginForm 
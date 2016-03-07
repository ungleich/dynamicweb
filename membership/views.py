from django.shortcuts import render, redirect
from django.views.generic import View

from .models import CustomUser
from .forms import LoginForm, RegisterForm


def validate_email(request, validate_slug):
    validated = User.validate_url(validate_slug)
    if validated:
        return render(request,'templates/validated.html')
    else:
        return render(request,'templates/error.html')


class LoginRegistrationView(View):
    def get(self, request):
        login_form = LoginForm()
        register_form = RegisterForm()
        if request.user.is_authenticated():
            return redirect("membership")
        else:
            return render(request, 'templates/login.html', {'login_form': login_form, 'register_form': register_form})

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        name = request.POST.get('name')
        if name and email and password:
            user = CustomUser.register(name, password,email)
            if user:
                return render(request, 'templates/success.html')
            else:
                return render(request, 'templates/error.html')

        elif email and password and not name:
            user = CustomUser.authenticate(email, password)
            if user:
                return redirect('membership')
            else:
                return render(request, 'templates/login', {'msg': 'Wrong username or password'})

class MembershipView(View):
    def get(self,request):
        return render(request,'templates/membership.html')

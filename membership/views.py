from django.shortcuts import render, redirect
from django.views.generic import View
from django.views.decorators.cache import cache_control
from django.conf import settings
from django.db.models import Q
from django.utils.translation import get_language
from django.contrib.auth import logout
from django.http import HttpResponseRedirect
from django.contrib.auth import login

from .models import CustomUser, StripeCustomer
from .forms import LoginForm, RegisterForm, PaymentForm
from utils.stripe_utils import StripeUtils


def validate_email(request, validate_slug):
    validated = CustomUser.validate_url(validate_slug)
    if validated:
        return render(request, 'templates/validated_email.html', {'msg': True})
    else:
        return render(request, 'templates/error.html', {'msg': 'Validation failed.'})


def reset(request, time):
    request.session['next'] = 0
    return redirect('payment', time=time)


class CreditCardView(View):
    def _get_context(self, request, time):
        request.session['time'] = time
        context = {}
        context['name'] = request.user.name
        if time == 'month':
            context['time'] = "1 month"
            context['price'] = "35"
            context['free'] = "1"
        elif time == 'year':
            context['time'] = '1 year'
            context['price'] = '360'
            context['free'] = "2"
        context['stripe_key'] = settings.STRIPE_API_PUBLIC_KEY
        context['form'] = PaymentForm()
        return context

    @cache_control(no_cache=True, must_revalidate=True)
    def get(self, request, time=None):
        context = self._get_context(request, time)
        next = request.session.get('next')
        if next == 1 or next == 0:
            template = 'templates/creditcard.html'
            request.session['next'] += 1
        elif next == 2:
            customer = StripeCustomer.get_or_create(email=request.user.email, token=request.session['token'])
            stripe_utils = StripeUtils()
            charge = stripe_utils.make_charge(request.session['amount'], customer=customer.stripe_id)
            template = 'templates/validated.html'
            resp = charge.get('response_object')
            context['msg'] = resp.get('status', None)
            request.session['next'] = None
        return render(request, template, context)

    def post(self, request, time=None):
        form = PaymentForm(request.POST)
        stripe_token = request.POST['stripeToken']

        if form.is_valid():
            form.save(request.user)
            amount = 35 if time == 'month' else 360
            request.session['token'] = stripe_token
            request.session['amount'] = amount
            request.session['next'] += 1
            return render(request, 'templates/confirm.html',
                          context={'name': request.user.name, 'email': request.user.email})
        else:
            context = self._get_context(request, time)
            context['form'] = form
            return render(request, 'templates/creditcard.html', context=context)


class LoginRegistrationView(View):
    def get(self, request):
        login_form = LoginForm()
        register_form = RegisterForm()
        request.session['next'] = None
        if request.user.is_authenticated():
            return redirect("membership")
        else:
            return render(request, 'templates/login.html',
                          {'login_form': login_form, 'register_form': register_form})

    def post(self, request):
        is_login = request.POST.get('is_login', False)

        if not is_login:
            form = RegisterForm(request.POST)
            if form.is_valid():
                email = form.validated_data.get('email')
                password = form.validated_data.get('password')
                name = form.validated_data.get('name')
                user = CustomUser.register(name, password, email)
                if user:
                    return render(request, 'templates/success.html')
                else:
                    return render(request, 'templates/error.html')
            else:
                login_form = LoginForm()
                return render(request, 'templates/login.html',
                              context={'login_form': login_form, 'register_form': form})
        else:
            form = LoginForm(request.POST)
            if form.is_valid():
                user = form.login(request)
                if user:
                    login(request, user)
                    return redirect('membership')
            else:
                registration_form = RegisterForm()
                return render(request, 'templates/login.html',
                              context={'login_form': form, 'register_form': registration_form})


class MembershipView(View):
    def get(self, request):
        # if the user has payed already
        member_payed = request.user.creditcards_set.filter(Q(payment_type='month') | Q(payment_type='year'))
        if member_payed:
            return redirect('/')
        request.session['next'] = 0
        language = get_language()
        return render(request, 'templates/membership.html', context={'language_code': language})


def logout_glarus(request):
    logout(request)
    return HttpResponseRedirect('/digitalglarus')

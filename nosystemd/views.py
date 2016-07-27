from django.views.generic import TemplateView, CreateView, FormView, DetailView, UpdateView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages


from membership.models import CustomUser, StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin
from utils.forms import PasswordResetRequestForm

from .forms import LoginForm, SignupForm, DonationForm, DonationBillingForm
from .models import Donation, DonatorStatus


class LandingView(TemplateView):
    template_name = "nosystemd/landing.html"


class LoginView(FormView):
    template_name = "nosystemd/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('nosystemd:landing')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth_user = authenticate(email=email, password=password)

        if auth_user:
            login(self.request, auth_user)
            return HttpResponseRedirect(self.get_success_url())

        return HttpResponseRedirect(self.get_success_url())

    def get(self, request, *args, **kwargs):
        if self.request.user.is_authenticated():
            return HttpResponseRedirect(reverse('nosystemd:landing'))
        return super(LoginView, self).get(request, *args, **kwargs)


class SignupView(CreateView):
    template_name = 'nosystemd/signup.html'
    model = CustomUser
    form_class = SignupForm

    def get_success_url(self):
        next_url = self.request.session.get('next', reverse_lazy('nosystemd:signup'))
        return next_url

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')

        CustomUser.register(name, password, email)
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)

        return HttpResponseRedirect(self.get_success_url())


class PasswordResetView(PasswordResetViewMixin):
    template_name = 'nosystemd/reset_password.html'
    success_url = reverse_lazy('nosystemd:login')
    form_class = PasswordResetRequestForm
    template_email_path = 'nosystemd/emails/'


class PasswordResetConfirmView(PasswordResetConfirmViewMixin):
    template_name = 'nosystemd/confirm_reset_password.html'
    success_url = reverse_lazy('nosystemd:login')


class DonationView(LoginRequiredMixin, FormView):
    template_name = 'nosystemd/donation.html'
    login_url = reverse_lazy('nosystemd:login')
    form_class = DonationBillingForm
    success_url = reverse_lazy('nosystemd:donations')

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })

        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            context = self.get_context_data()
            token = form.cleaned_data.get('token')
            donation_amount = form.cleaned_data.get('donation_amount')

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=self.request.user.email,
                                                    token=token)
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(self.get_context_data(form=form))

            # Create Billing Address
            billing_address = form.save()

            # Make stripe charge to a customer
            stripe_utils = StripeUtils()
            stripe_utils.CURRENCY = 'usd'
            charge_response = stripe_utils.make_charge(amount=donation_amount,
                                                       customer=customer.stripe_id)
            charge = charge_response.get('response_object')

            # Check if the payment was approved
            if not charge:
                context.update({
                    'paymentError': charge_response.get('error'),
                    'form': form
                })
                return render(request, self.template_name, context)

            # Create a donation
            charge = charge_response.get('response_object')
            donation_data = request.POST.copy()
            donation_data.update({
                'cc_brand': charge.source.brand,
                'stripe_charge_id': charge.id,
                'last4': charge.source.last4,
                'billing_address': billing_address.id,
                'donator': customer.id,
                'donation': donation_amount
            })
            donation_form = DonationForm(donation_data)
            if donation_form.is_valid():
                donation = donation_form.save()
                return HttpResponseRedirect(reverse('nosystemd:donations',
                                                    kwargs={'pk': donation.id}))
            else:
                self.form_invalid(donation_form)

        else:
            return self.form_invalid(form)


class DonationDetailView(LoginRequiredMixin, DetailView):
    template_name = "nosystemd/donation_detail.html"
    context_object_name = "donation"
    login_url = reverse_lazy('nosystemd:login')
    model = Donation


class DonatorStatusDetailView(LoginRequiredMixin, TemplateView):
    template_name = "nosystemd/donator_status.html"
    login_url = reverse_lazy('nosystemd:login')
    model = DonatorStatus

    def get_context_data(self, **kwargs):
        context = super(DonatorStatusDetailView, self).get_context_data(**kwargs)
        context.update({
            'donator_status': self.request.user.donatorstatus
            if self.request.user.donatorstatus else None
        })
        return context

    def get(self, request, *args, **kwargs):
        if not request.user.donatorstatus:
            HttpResponseRedirect('nosystemd:landing')
        return super(DonatorStatusDetailView, self).get(request, *args, **kwargs)


class ChangeDonatorStatusDetailView(LoginRequiredMixin, UpdateView):
    template_name = "nosystemd/donator_status.html"
    context_object_name = "donator_status"
    login_url = reverse_lazy('nosystemd:login')
    model = DonatorStatus

    def get_object(self, queryset=None):
        return self.request.user.donatorstatus

    def post(self, *args, **kwargs):
        donator_status = self.get_object()

        donator_status.status = DonatorStatus.ACTIVE \
            if donator_status.status == DonatorStatus.CANCELED else DonatorStatus.CANCELED

        donator_status.save()
        messages.success(self.request, 'Your monthly donation status has been changed.')
        return HttpResponseRedirect(reverse_lazy('nosystemd:donator_status'))

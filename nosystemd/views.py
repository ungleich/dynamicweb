from django.views.generic import TemplateView, FormView, DetailView, UpdateView,\
    ListView
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings
from django.contrib import messages


from membership.models import StripeCustomer
from utils.stripe_utils import StripeUtils
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin, LoginViewMixin,\
    SignupViewMixin
from utils.forms import PasswordResetRequestForm
from utils.mailer import BaseEmail

from .forms import LoginForm, SignupForm, DonationForm, DonationBillingForm
from .models import Donation, DonatorStatus


class LandingView(TemplateView):
    template_name = "nosystemd/landing.html"

    def get_context_data(self, *args, **kwargs):

        allow_donation = self.request.user.is_anonymous() or \
            (self.request.user.is_authenticated() and
             not DonatorStatus.objects.filter(user=self.request.user).exists())

        total_donations_amount = Donation.get_total_donations_amount()
        context = {
            'total_donations_amount': total_donations_amount,
            'allow_donation': allow_donation
        }
        return context


class LoginView(LoginViewMixin):
    template_name = "nosystemd/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('nosystemd:landing')


class SignupView(SignupViewMixin):
    template_name = "nosystemd/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('nosystemd:landing')


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
    form_class = DonationBillingForm
    success_url = reverse_lazy('nosystemd:make_donation')

    def get_login_url(self):
        return "%s?next=%s" % (reverse('nosystemd:signup'),
                               reverse('nosystemd:make_donation'))

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })

        return context

    def get(self, request, *args, **kwargs):

        # if DonatorStatus.objects.filter(user=self.request.user).exists():
        #     messages.success(self.request, 'Your already are a monthly contributor')
        #     return HttpResponseRedirect(reverse_lazy('nosystemd:donations'))

        return self.render_to_response(self.get_context_data())

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

                # reactivate donation status
                donation = donation_form.save()

                try:
                    donator_status = DonatorStatus.objects.get(user=self.request.user)
                    donator_status.set_active()
                except DonatorStatus.DoesNotExist:
                    pass

                donation = donation_form.save()

                context = {
                    'donation': donation,
                    'base_url': "{0}://{1}".format(request.scheme, request.get_host())

                }
                email_data = {
                    'subject': 'Your donation have been charged',
                    'to': request.user.email,
                    'context': context,
                    'template_name': 'donation_charge',
                    'template_path': 'nosystemd/emails/'
                }
                email = BaseEmail(**email_data)
                email.send()

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


class DonationListView(LoginRequiredMixin, ListView):
    template_name = "nosystemd/donations.html"
    context_object_name = "donations"
    login_url = reverse_lazy('nosystemd:login')
    model = Donation
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(DonationListView, self).get_context_data(**kwargs)

        status = None
        try:
            status = self.request.user.donatorstatus
        except DonatorStatus.DoesNotExist:
            pass

        context.update({
            'donator_status': status
        })
        return context

    def get_queryset(self):
        queryset = super(DonationListView, self).get_queryset()
        queryset = queryset.filter(donator__user=self.request.user)
        return queryset


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
        return HttpResponseRedirect(reverse_lazy('nosystemd:donations'))

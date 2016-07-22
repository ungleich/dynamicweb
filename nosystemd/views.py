from django.views.generic import TemplateView, CreateView, FormView
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.conf import settings

from membership.models import CustomUser
from utils.views import PasswordResetViewMixin, PasswordResetConfirmViewMixin
from utils.forms import PasswordResetRequestForm, BillingAddressForm

from .forms import LoginForm, SignupForm


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
    form_class = BillingAddressForm

    def get_context_data(self, **kwargs):
        context = super(DonationView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })

        return context

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()

    #     if form.is_valid():
    #         context = self.get_context_data()
    #         specifications = request.session.get('vm_specs')
    #         vm_type = specifications.get('hosting_company')
    #         vm = VirtualMachineType.objects.get(hosting_company=vm_type)
    #         final_price = vm.calculate_price(specifications)

    #         plan_data = {
    #             'vm_type': vm,
    #             'cores': specifications.get('cores'),
    #             'memory': specifications.get('memory'),
    #             'disk_size': specifications.get('disk_size'),
    #             'configuration': specifications.get('configuration'),
    #             'price': final_price
    #         }
    #         token = form.cleaned_data.get('token')

    #         # Get or create stripe customer
    #         customer = StripeCustomer.get_or_create(email=self.request.user.email,
    #                                                 token=token)
    #         if not customer:
    #             form.add_error("__all__", "Invalid credit card")
    #             return self.render_to_response(self.get_context_data(form=form))

    #         # Create Virtual Machine Plan
    #         plan = VirtualMachinePlan.create(plan_data, request.user)

    #         # Create Billing Address
    #         billing_address = form.save()

    #         # Create a Hosting Order
    #         order = HostingOrder.create(vm_plan=plan, customer=customer,
    #                                     billing_address=billing_address)

    #         # Make stripe charge to a customer
    #         stripe_utils = StripeUtils()
    #         charge_response = stripe_utils.make_charge(amount=final_price,
    #                                                    customer=customer.stripe_id)
    #         charge = charge_response.get('response_object')

    #         # Check if the payment was approved
    #         if not charge:
    #             context.update({
    #                 'paymentError': charge_response.get('error'),
    #                 'form': form
    #             })
    #             return render(request, self.template_name, context)

    #         charge = charge_response.get('response_object')

    #         # Associate an order with a stripe payment
    #         order.set_stripe_charge(charge)

    #         # If the Stripe payment was successed, set order status approved
    #         order.set_approved()

    #         # Send notification to ungleich as soon as VM has been booked
    #         # TODO send email using celery

    #         context = {
    #             'vm': plan,
    #             'order': order,
    #             'base_url': "{0}://{1}".format(request.scheme, request.get_host())

    #         }
    #         email_data = {
    #             'subject': 'New VM request',
    #             'to': request.user.email,
    #             'context': context,
    #             'template_name': 'new_booked_vm',
    #             'template_path': 'hosting/emails/'
    #         }
    #         email = BaseEmail(**email_data)
    #         email.send()

    #         return HttpResponseRedirect(reverse('hosting:orders', kwargs={'pk': order.id}))
    #     else:
    #         return self.form_invalid(form)



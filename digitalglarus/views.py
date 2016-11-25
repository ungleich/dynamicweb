import json
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import get_language
from djangocms_blog.models import Post
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View, DetailView, ListView


from .models import Supporter
from .mixins import ChangeMembershipStatusMixin
from utils.forms import ContactUsForm
from utils.mailer import BaseEmail

from django.views.generic.edit import FormView
from membership.calendar.calendar import BookCalendar
from membership.models import Calendar as CalendarModel, StripeCustomer


from utils.views import LoginViewMixin, SignupViewMixin, \
    PasswordResetViewMixin, PasswordResetConfirmViewMixin
from utils.forms import PasswordResetRequestForm, UserBillingAddressForm
from utils.stripe_utils import StripeUtils
from utils.models import UserBillingAddress


from .forms import LoginForm, SignupForm, MembershipBillingForm, BookingDateForm,\
    BookingBillingForm

from .models import MembershipType, Membership, MembershipOrder, Booking, BookingPrice,\
    BookingOrder

from .mixins import MembershipRequiredMixin, IsNotMemberMixin


class IndexView(TemplateView):
    template_name = "digitalglarus/index.html"


class SupportusView(TemplateView):
    template_name = "digitalglarus/supportus.html"

    def get_context_data(self, *args, **kwargs):
        context = super(SupportusView, self).get_context_data(**kwargs)
        tags = ["dg-renovation"]
        posts = Post.objects.filter(tags__name__in=tags, publish=True).translated(get_language())
        context.update({
            'post_list': posts
        })
        return context


class LoginView(LoginViewMixin):
    template_name = "digitalglarus/login.html"
    form_class = LoginForm

    def get_success_url(self):
        # redirect to membership orders list if user has at least one.
        if self.request.user \
           and MembershipOrder.objects.filter(customer__user=self.request.user):

            return reverse_lazy('digitalglarus:membership_orders_list')

        return reverse_lazy('digitalglarus:membership_pricing')


class SignupView(SignupViewMixin):
    template_name = "digitalglarus/signup.html"
    form_class = SignupForm
    success_url = reverse_lazy('digitalglarus:login')


class PasswordResetView(PasswordResetViewMixin):
    template_name = 'digitalglarus/reset_password.html'
    success_url = reverse_lazy('digitalglarus:login')
    form_class = PasswordResetRequestForm
    template_email_path = 'digitalglarus/emails/'


class PasswordResetConfirmView(PasswordResetConfirmViewMixin):
    template_name = 'digitalglarus/confirm_reset_password.html'
    success_url = reverse_lazy('digitalglarus:login')


class HistoryView(TemplateView):
    template_name = "digitalglarus/history.html"

    def get_context_data(self, *args, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        supporters = Supporter.objects.all()
        context.update({
            'supporters': supporters
        })
        return context


class BookingSelectDatesView(LoginRequiredMixin, MembershipRequiredMixin, FormView):
    template_name = "digitalglarus/booking.html"
    form_class = BookingDateForm
    membership_redirect_url = reverse_lazy('digitalglarus:membership_pricing')
    login_url = reverse_lazy('digitalglarus:login')
    success_url = reverse_lazy('digitalglarus:booking_payment')

    def get_form_kwargs(self):
        kwargs = super(BookingSelectDatesView, self).get_form_kwargs()
        kwargs.update({'user': self.request.user})
        return kwargs

    def form_valid(self, form):
        user = self.request.user
        start_date = form.cleaned_data.get('start_date')
        end_date = form.cleaned_data.get('end_date')
        booking_days = (end_date - start_date).days + 1

        price_per_day = BookingPrice.objects.get().price_per_day

        original_price, final_price, free_days = Booking.\
            booking_price(user, start_date, end_date)

        total_discount = price_per_day * free_days

        self.request.session.update({
            'original_price': original_price,
            'final_price': final_price,
            'total_discount': total_discount,
            'booking_price_per_day': price_per_day,
            'booking_days': booking_days,
            'free_days': free_days,
            'start_date': start_date.strftime('%m/%d/%Y'),
            'end_date': end_date.strftime('%m/%d/%Y'),
            'is_free': final_price == 0
        })
        return super(BookingSelectDatesView, self).form_valid(form)


class BookingPaymentView(LoginRequiredMixin, MembershipRequiredMixin, FormView):
    template_name = "digitalglarus/booking_payment.html"
    form_class = BookingBillingForm
    membership_redirect_url = reverse_lazy('digitalglarus:membership_pricing')
    # success_url = reverse_lazy('digitalglarus:booking_payment')
    booking_needed_fields = ['original_price', 'final_price', 'booking_days', 'free_days',
                             'start_date', 'end_date', 'booking_price_per_day',
                             'total_discount', 'is_free']

    def dispatch(self, request, *args, **kwargs):
        from_booking = all(field in request.session.keys()
                           for field in self.booking_needed_fields)
        if not from_booking:
            return HttpResponseRedirect(reverse('digitalglarus:booking'))

        return super(BookingPaymentView, self).dispatch(request, *args, **kwargs)

    def get_success_url(self, order_id):
        return reverse('digitalglarus:booking_orders_detail', kwargs={'pk': order_id})

    def get_form_kwargs(self):
        current_billing_address = self.request.user.billing_addresses.first()
        form_kwargs = super(BookingPaymentView, self).get_form_kwargs()
        form_kwargs.update({
            'initial': {
                'start_date': self.request.session.get('start_date'),
                'end_date': self.request.session.get('end_date'),
                'price': self.request.session.get('final_price'),
                'street_address': current_billing_address.street_address,
                'city': current_billing_address.city,
                'postal_code': current_billing_address.postal_code,
                'country': current_billing_address.country,
            }
        })
        return form_kwargs

    def get_context_data(self, *args, **kwargs):
        context = super(BookingPaymentView, self).get_context_data(*args, **kwargs)

        booking_data = {key: self.request.session.get(key)
                        for key in self.booking_needed_fields}
        user = self.request.user
        last_booking_order = BookingOrder.objects.filter(customer__user=user).last()
        last_membership_order = MembershipOrder.objects.filter(customer__user=user).last()
        credit_card_data = last_booking_order.get_booking_cc_data() if last_booking_order \
            and last_booking_order.get_booking_cc_data() \
            else last_membership_order.get_membership_order_cc_data()

        booking_data.update({
            'credit_card_data': credit_card_data if credit_card_data else None,
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })
        context.update(booking_data)
        return context

    def form_valid(self, form):
        data = form.cleaned_data
        context = self.get_context_data()
        token = data.get('token')
        start_date = data.get('start_date')
        end_date = data.get('end_date')
        is_free = context.get('is_free')
        normal_price, final_price, free_days = Booking.\
            booking_price(self.request.user, start_date, end_date)
        charge = None

        # if not credit_card_needed:
        # Get or create stripe customer
        customer = StripeCustomer.get_or_create(email=self.request.user.email,
                                                token=token)
        if not customer:
            form.add_error("__all__", "Invalid credit card")
            return self.render_to_response(self.get_context_data(form=form))

        # If booking is not free, make the stripe charge
        if not is_free:
            # Make stripe charge to a customer
            stripe_utils = StripeUtils()
            charge_response = stripe_utils.make_charge(amount=final_price,
                                                       customer=customer.stripe_id)
            charge = charge_response.get('response_object')

            # Check if the payment was approved
            if not charge:
                context.update({
                    'paymentError': charge_response.get('error'),
                    'form': form
                })
                return render(self.request, self.template_name, context)

            charge = charge_response.get('response_object')

        # Create Billing Address for Membership Order
        billing_address = form.save()

        # Create Billing Address for User if he does not have one
        if not customer.user.billing_addresses.count():
            data.update({
                'user': customer.user.id
            })
            billing_address_user_form = UserBillingAddressForm(data)
            billing_address_user_form.is_valid()
            billing_address_user_form.save()

        # Create Booking
        booking_data = {
            'start_date': start_date,
            'end_date': end_date,
            'start_date': start_date,
            'free_days': free_days,
            'price': normal_price,
            'final_price': final_price,
        }
        booking = Booking.create(booking_data)

        # Create Booking order
        order_data = {
            'booking': booking,
            'customer': customer,
            'billing_address': billing_address,
            'stripe_charge': charge,
            'amount': final_price,
            'original_price': normal_price,
            'special_month_price': BookingPrice.objects.last().special_month_price,
        }
        order = BookingOrder.create(order_data)

        context = {
            'booking': booking,
            'order': order,
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        }

        email_data = {
            'subject': 'Your booking order has been placed',
            'to': self.request.user.email,
            'context': context,
            'template_name': 'booking_order_email',
            'template_path': 'digitalglarus/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        return HttpResponseRedirect(self.get_success_url(order.id))


class MembershipPricingView(TemplateView):
    template_name = "digitalglarus/membership_pricing.html"

    def get_context_data(self, **kwargs):
        context = super(MembershipPricingView, self).get_context_data(**kwargs)
        membership_type = MembershipType.objects.last()
        context.update({
            'membership_type': membership_type
        })
        return context


class MembershipPaymentView(LoginRequiredMixin, IsNotMemberMixin, FormView):
    template_name = "digitalglarus/membership_payment.html"
    login_url = reverse_lazy('digitalglarus:signup')
    form_class = MembershipBillingForm
    already_member_redirect_url = reverse_lazy('digitalglarus:membership_orders_list')

    def get_form_kwargs(self):
        self.membership_type = MembershipType.objects.get(name='standard')
        form_kwargs = super(MembershipPaymentView, self).get_form_kwargs()
        form_kwargs.update({
            'initial': {
                'membership_type': self.membership_type.id
            }
        })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(MembershipPaymentView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY,
            'membership_type': self.membership_type
        })
        return context

    def post(self, request, *args, **kwargs):
        form = self.get_form()

        if form.is_valid():
            data = form.cleaned_data
            context = self.get_context_data()
            token = data.get('token')
            membership_type = data.get('membership_type')

            # Get or create stripe customer
            customer = StripeCustomer.get_or_create(email=self.request.user.email,
                                                    token=token)
            if not customer:
                form.add_error("__all__", "Invalid credit card")
                return self.render_to_response(self.get_context_data(form=form))

            # Make stripe charge to a customer
            stripe_utils = StripeUtils()
            charge_response = stripe_utils.make_charge(amount=membership_type.first_month_price,
                                                       customer=customer.stripe_id)
            charge = charge_response.get('response_object')

            # Check if the payment was approved
            if not charge:
                context.update({
                    'paymentError': charge_response.get('error'),
                    'form': form
                })
                return render(request, self.template_name, context)

            charge = charge_response.get('response_object')

            # Create Billing Address
            billing_address = form.save()

            # Create Billing Address for User if he does not have one
            if not customer.user.billing_addresses.count():
                data.update({
                    'user': customer.user.id
                })
                billing_address_user_form = UserBillingAddressForm(data)
                billing_address_user_form.is_valid()
                billing_address_user_form.save()

            # Get membership dates
            membership_start_date, membership_end_date = membership_type.first_month_range

            # Create or update membership plan
            membership_data = {
                'type': membership_type,
                'active': True,
                'start_date': membership_start_date,
                'end_date': membership_end_date
            }
            membership = Membership.activate_or_crete(membership_data, self.request.user)

            # Create membership order
            order_data = {
                'membership': membership,
                'customer': customer,
                'billing_address': billing_address,
                'stripe_charge': charge,
                'amount': membership_type.first_month_price,
                'start_date': membership_start_date,
                'end_date': membership_end_date
            }

            membership_order = MembershipOrder.create(order_data)

            request.session.update({
                'membership_price': membership.type.first_month_price,
                'membership_dates': membership.type.first_month_formated_range
            })

            context = {
                'membership': membership,
                'order': membership_order,
                'membership_start_date': membership_start_date,
                'membership_end_date': membership_end_date,
                'base_url': "{0}://{1}".format(request.scheme, request.get_host())

            }
            email_data = {
                'subject': 'Your membership has been charged',
                'to': request.user.email,
                'context': context,
                'template_name': 'membership_charge',
                'template_path': 'digitalglarus/emails/'
            }
            email = BaseEmail(**email_data)
            email.send()

            return HttpResponseRedirect(reverse('digitalglarus:membership_activated'))

        else:
            return self.form_invalid(form)


class MembershipActivatedView(TemplateView):
    template_name = "digitalglarus/membership_activated.html"

    def get_context_data(self, **kwargs):
        context = super(MembershipActivatedView, self).get_context_data(**kwargs)
        membership_price = self.request.session.get('membership_price')
        membership_dates = self.request.session.get('membership_dates')
        context.update({
            'membership_price': membership_price,
            'membership_dates': membership_dates,
        })
        return context


class MembershipDeactivateView(LoginRequiredMixin, UpdateView):
    template_name = "digitalglarus/membership_deactivated.html"
    model = Membership
    success_message = "Your membership has been deactivated :("
    success_url = reverse_lazy('digitalglarus:membership_orders_list')
    login_url = reverse_lazy('digitalglarus:login')
    fields = '__all__'

    def get_object(self):
        membership_order = MembershipOrder.objects.\
            filter(customer__user=self.request.user).last()
        if not membership_order:
            raise AttributeError("Membership does not exists")
        membership = membership_order.membership
        return membership

    def post(self, *args, **kwargs):
        membership = self.get_object()
        membership.deactivate()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)

        return HttpResponseRedirect(self.success_url)


class MembershipReactivateView(ChangeMembershipStatusMixin):
    success_message = "Your membership has been reactivate :)"
    template_name = "digitalglarus/membership_orders_list.html"

    def post(self, request, *args, **kwargs):
        membership = self.get_object()
        membership.activate()
        return super(MembershipReactivateView, self).post(request, *args, **kwargs)


class UserBillingAddressView(LoginRequiredMixin, UpdateView):
    model = UserBillingAddress
    form_class = UserBillingAddressForm
    template_name = "digitalglarus/user_billing_address.html"
    success_url = reverse_lazy('digitalglarus:user_billing_address')
    success_message = "Billing Address Updated"

    def get_success_url(self):
        next_url = self.request.POST.get('next') if self.request.POST.get('next')\
            else self.success_url

        return next_url

    def form_valid(self, form):
        """
        If the form is valid, save the associated model.
        """
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        self.object = form.save()
        return super(UserBillingAddressView, self).form_valid(form)

    def get_form_kwargs(self):
        current_billing_address = self.request.user.billing_addresses.first()
        form_kwargs = super(UserBillingAddressView, self).get_form_kwargs()

        if not current_billing_address:
            return form_kwargs

        form_kwargs.update({
            'initial': {
                'street_address': current_billing_address.street_address,
                'city': current_billing_address.city,
                'postal_code': current_billing_address.postal_code,
                'country': current_billing_address.country,
            }
        })
        return form_kwargs

    def get_object(self):
        current_billing_address = self.request.user.billing_addresses.filter(current=True).last()
        if not current_billing_address:
            raise AttributeError("Billing Address does not exists")
        return current_billing_address


class MembershipDeactivateSuccessView(LoginRequiredMixin, TemplateView):
    template_name = "digitalglarus/membership_deactivated_success.html"


class MembershipOrdersListView(LoginRequiredMixin, ListView):
    template_name = "digitalglarus/membership_orders_list.html"
    context_object_name = "orders"
    login_url = reverse_lazy('digitalglarus:login')
    model = MembershipOrder
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(MembershipOrdersListView, self).get_context_data(**kwargs)
        current_membership = Membership.get_current_membership(self.request.user)
        start_date, end_date = (current_membership.start_date, current_membership.end_date)\
            if current_membership else [None, None]

        next_start_date, next_end_date = MembershipOrder.next_membership_dates(self.request.user)
        current_billing_address = self.request.user.billing_addresses.filter(current=True).last()
        context.update({
            'membership_start_date': start_date,
            'membership_end_date': end_date,
            'current_membership': current_membership,
            'next_membership_start_date': next_start_date,
            'next_membership_end_date': next_end_date,
            'billing_address': current_billing_address
        })
        return context

    def get_queryset(self):
        queryset = super(MembershipOrdersListView, self).get_queryset()
        queryset = queryset.filter(customer__user=self.request.user)
        return queryset


class OrdersMembershipDetailView(LoginRequiredMixin, DetailView):
    template_name = "digitalglarus/membership_orders_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('digitalglarus:login')
    # permission_required = ['view_hostingorder']
    model = MembershipOrder

    def get_context_data(self, **kwargs):
        context = super(OrdersMembershipDetailView, self).get_context_data(**kwargs)
        start_date, end_date = self.object.get_membership_range_date()
        context.update({
            'membership_start_date': start_date,
            'membership_end_date': end_date,
        })
        return context


class OrdersBookingDetailView(LoginRequiredMixin, DetailView):
    template_name = "digitalglarus/booking_orders_detail.html"
    context_object_name = "order"
    login_url = reverse_lazy('digitalglarus:login')
    # permission_required = ['view_hostingorder']
    model = BookingOrder

    def get_context_data(self, *args, **kwargs):

        context = super(OrdersBookingDetailView, self).get_context_data(**kwargs)

        bookig_order = self.object
        booking = bookig_order.booking

        start_date = booking.start_date
        end_date = booking.end_date
        free_days = booking.free_days

        booking_days = (end_date - start_date).days + 1
        original_price = booking.price
        final_price = booking.final_price

        context.update({
            'original_price': original_price,
            'total_discount': original_price - final_price,
            'final_price': final_price,
            'booking_days': booking_days,
            'free_days': free_days,
            'start_date': start_date.strftime('%m/%d/%Y'),
            'end_date': end_date.strftime('%m/%d/%Y'),
        })

        return context


class BookingOrdersListView(LoginRequiredMixin, ListView):
    template_name = "digitalglarus/booking_orders_list.html"
    context_object_name = "orders"
    login_url = reverse_lazy('digitalglarus:login')
    model = BookingOrder
    paginate_by = 10

    def get_context_data(self, **kwargs):
        context = super(BookingOrdersListView, self).get_context_data(**kwargs)
        current_billing_address = self.request.user.billing_addresses.filter(current=True).last()
        context.update({
            'billing_address': current_billing_address
        })
        return context

    def get_queryset(self):
        queryset = super(BookingOrdersListView, self).get_queryset()
        queryset = queryset.filter(customer__user=self.request.user)
        return queryset


############## OLD VIEWS 
class CalendarApi(View):
    def get(self,request,month,year):
        calendar = BookCalendar(request.user,requested_month=month).formatmonth(int(year),int(month))
        ret = {'calendar':calendar,'month':month,'year':year}
        return JsonResponse(ret)

    def post(self,request):
        pd = json.loads(request.POST.get('data',''))
        ret = {'status':'success'}
        CalendarModel.add_dates(pd,request.user)
        return JsonResponse(ret)

class ContactView(FormView):
    template_name = 'contact.html'
    form_class = ContactUsForm
    success_url = reverse_lazy('digitalglarus:contact')
    success_message = _('Message Successfully Sent')

    def form_valid(self, form):
        form.save()
        form.send_email()
        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(ContactView, self).form_valid(form)


class AboutView(TemplateView):
    template_name = "digitalglarus/about.html"

def detail(request, message_id):
    p = get_object_or_404(Message, pk=message_id)

    context = { 'message': p, }
    return render(request, 'digitalglarus/detail.html', context)

def about(request):
    return render(request, 'digitalglarus/about.html')

def home(request):
    return render(request, 'index.html')

def letscowork(request):
    return render(request, 'digitalglarus/letscowork.html')


def blog(request):
    tags = ["digitalglarus"]
    posts = Post.objects.filter(tags__name__in=tags, publish=True).translated(get_language())
    # posts = Post.objects.filter_by_language(get_language()).filter(tags__name__in=tags, publish=True)
    context = {
        'post_list': posts,
    }
    return render(request, 'glarus_blog/post_list.html', context)


def blog_detail(request, slug):
    # post = Post.objects.filter_by_language(get_language()).filter(slug=slug).first()

    post = Post.objects.translated(get_language(), slug=slug).first()
    context = {
        'post': post,
    }
    return render(request, 'glarus_blog/post_detail.html', context)


def support(request):
    return render(request, 'support.html')


def supporters(request):
    context = {
        'supporters': Supporter.objects.order_by('name')
    }
    return render(request, 'supporters.html', context)




import json
import datetime

from django.conf import settings
from django.shortcuts import get_object_or_404, render
from django.forms import ModelForm
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse_lazy, reverse
from django.utils.translation import ugettext_lazy as _
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.translation import get_language
from djangocms_blog.models import Post
from django.contrib import messages
from django.http import JsonResponse
from django.views.generic import View

from .models import Supporter
from utils.forms import ContactUsForm
from django.views.generic.edit import FormView
from membership.calendar.calendar import BookCalendar
from membership.models import Calendar as CalendarModel, CustomUser, StripeCustomer


from utils.views import LoginViewMixin, SignupViewMixin, \
    PasswordResetViewMixin, PasswordResetConfirmViewMixin
from utils.forms import PasswordResetRequestForm
from utils.stripe_utils import StripeUtils


from .forms import LoginForm, SignupForm, MembershipBillingForm
from .models import MembershipType


class IndexView(TemplateView):
    template_name = "digitalglarus/old_index.html"


class LoginView(LoginViewMixin):
    template_name = "digitalglarus/login.html"
    form_class = LoginForm
    success_url = reverse_lazy('digitalglarus:landing')


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

    def get_context_data(self, **kwargs):
        context = super(HistoryView, self).get_context_data(**kwargs)
        supporters = Supporter.objects.all()
        context.update({
            'supporters': supporters
        })
        return context


class MembershipPaymentView(LoginRequiredMixin, FormView):
    template_name = "digitalglarus/membership_payment.html"
    login_url = reverse_lazy('digitalglarus:login')
    form_class = MembershipBillingForm

    def get_form_kwargs(self):
        membership_type = MembershipType.objects.get(name='standard')
        form_kwargs = super(MembershipPaymentView, self).get_form_kwargs()
        form_kwargs.update({
            'initial': {'membership_type': membership_type.id}
        })
        return form_kwargs

    def get_context_data(self, **kwargs):
        context = super(MembershipPaymentView, self).get_context_data(**kwargs)
        context.update({
            'stripe_key': settings.STRIPE_API_PUBLIC_KEY
        })
        return context

    def post(self, request, *args, **kwargs):
        import pdb;pdb.set_trace()
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
            charge_response = stripe_utils.make_charge(amount=membership_type.price,
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
        else:
            return self.form_invalid(form)



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




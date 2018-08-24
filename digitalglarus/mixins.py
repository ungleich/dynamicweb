from django.core.urlresolvers import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.db import models
from django.http import HttpResponseRedirect
from django.contrib import messages


from membership.models import StripeCustomer
from utils.models import BillingAddress


class MembershipRequiredMixin(object):
    membership_redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        from .models import Membership
        if not Membership.is_digitalglarus_active_member(request.user):
            return HttpResponseRedirect(self.membership_redirect_url)

        return super(MembershipRequiredMixin, self).dispatch(request, *args, **kwargs)


class IsNotMemberMixin(object):
    already_member_redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        from .models import Membership
        if Membership.is_digitalglarus_active_member(request.user):
            return HttpResponseRedirect(self.already_member_redirect_url)

        return super(IsNotMemberMixin, self).dispatch(request, *args, **kwargs)


class Ordereable(models.Model):
    customer = models.ForeignKey(StripeCustomer)
    amount = models.FloatField()
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4, blank=True)
    cc_brand = models.CharField(max_length=128, blank=True)
    stripe_charge_id = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, data):
        stripe_charge = data.pop('stripe_charge', None)
        instance = cls.objects.create(**data)
        if not stripe_charge:
            return instance
        instance.stripe_charge_id = stripe_charge.id
        instance.last4 = stripe_charge.source.last4
        instance.cc_brand = stripe_charge.source.brand
        instance.save()
        return instance


class ChangeMembershipStatusMixin(LoginRequiredMixin, UpdateView):
    success_message = None
    success_url = reverse_lazy('digitalglarus:membership_orders_list')
    login_url = reverse_lazy('digitalglarus:login')
    fields = '__all__'

    def get_object(self):
        from .models import MembershipOrder
        membership_order = MembershipOrder.objects.\
            filter(customer__user=self.request.user).last()
        if not membership_order:
            raise AttributeError("Membership does not exists")
        membership = membership_order.membership
        return membership

    def post(self, *args, **kwargs):
        membership = self.get_object()
        membership.activate()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)

        return HttpResponseRedirect(self.success_url)

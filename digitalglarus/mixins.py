from django.db import models
from django.http import HttpResponseRedirect
from membership.models import StripeCustomer
from utils.models import BillingAddress


class MembershipRequired(object):
    membership_redirect_url = None

    def dispatch(self, request, *args, **kwargs):
        from .models import Membership
        if not Membership.is_digitalglarus_member(request.user):
            return HttpResponseRedirect(self.membership_redirect_url)

        return super(MembershipRequired, self).dispatch(request, *args, **kwargs)


class Ordereable(models.Model):
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)

    class Meta:
        abstract = True

    @classmethod
    def create(cls, data):
        stripe_charge = data.pop('stripe_charge', None)
        instance = cls.objects.create(**data)
        instance.stripe_charge_id = stripe_charge.id
        instance.last4 = stripe_charge.source.last4
        instance.cc_brand = stripe_charge.source.brand
        instance.save()
        return instance

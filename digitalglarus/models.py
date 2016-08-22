
import calendar
from datetime import datetime, date, timedelta
from django.db import models
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property

from membership.models import StripeCustomer
from utils.models import BillingAddress


class MembershipType(models.Model):

    MEMBERSHIP_TYPES = (
        ('standard', 'Standard'),

    )
    name = models.CharField(choices=MEMBERSHIP_TYPES, max_length=20)
    price = models.FloatField()

    @cached_property
    def days_left(self):
        current_date = date.today()
        _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
        pass_days = current_date.day
        days_left = days_in_month - pass_days + 1
        return days_left

    @cached_property
    def first_month_price(self):
        current_date = date.today()
        _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
        pass_days = current_date.day
        days_left = days_in_month - pass_days + 1
        percentage = days_left / days_in_month
        membership_price = self.price
        final_price = membership_price * percentage
        return final_price

    @cached_property
    def first_month_range(self):
        current_date = date.today()
        _, days_in_month = calendar.monthrange(current_date.year, current_date.month)
        pass_days = current_date.day
        days_left = days_in_month - pass_days
        end_date = current_date + timedelta(days=days_left)
        return current_date, end_date

    @cached_property
    def first_month_formated_range(self):
        start_date, end_date = self.first_month_range
        return "{} - {}".format(datetime.strftime(start_date, "%b, %d %Y"),
                                datetime.strftime(end_date, "%b, %d %Y"))


class Membership(models.Model):
    type = models.ForeignKey(MembershipType)

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance


class MembershipOrder(models.Model):
    membership = models.ForeignKey(Membership)
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)

    @classmethod
    def create(cls, data):
        stripe_charge = data.pop('stripe_charge', None)
        instance = cls.objects.create(**data)
        instance.stripe_charge_id = stripe_charge.id
        instance.last4 = stripe_charge.source.last4
        instance.cc_brand = stripe_charge.source.brand
        return instance


class Supporter(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse('dgSupporters_view', args=[self.pk])


class DGGallery(models.Model):
    parent = models.ForeignKey('self', blank=True, null=True)
    name = models.CharField(max_length=30)

    def __str__(self):
        return "%s" % (self.name)

    def get_absolute_url(self):
        return reverse('dgGallery_view', args=[self.pk])

    class Meta:
        verbose_name_plural = 'dgGallery'
#
class DGPicture(models.Model):
    gallery = models.ForeignKey(DGGallery)
    image =  FilerImageField(related_name='dg_gallery')
    description = models.CharField(max_length=60)

    def __str__(self):
        return "%s" % (self.image.name)

class DGGalleryPlugin(CMSPlugin):
    dgGallery = models.ForeignKey(DGGallery)

class DGSupportersPlugin(CMSPlugin):
    pass

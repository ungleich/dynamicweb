
import calendar
from datetime import datetime, date, timedelta
from dateutil.relativedelta import relativedelta
from django.db import models
from django.db.models import Q
from cms.models import CMSPlugin
from filer.fields.image import FilerImageField
from django.core.urlresolvers import reverse
from django.utils.functional import cached_property
from .mixins import Ordereable

# from membership.models import StripeCustomer
# from utils.models import BillingAddress


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
    active = models.BooleanField(default=True)

    @classmethod
    def is_digitalglarus_member(cls, user):
        past_month = (datetime.today() - relativedelta(months=1)).month
        has_booking_current_month = Q(membershiporder__customer__user=user,
                                      membershiporder__created_at__month=datetime.today().month)
        has_booking_past_month = Q(membershiporder__customer__user=user,
                                   membershiporder__created_at__month=past_month)
        active_membership = Q(active=True)
        return cls.objects.filter(has_booking_past_month | has_booking_current_month).\
            filter(active_membership).exists()

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance

    def deactivate(self):
        self.active = False
        self.save()


class MembershipOrder(Ordereable, models.Model):
    membership = models.ForeignKey(Membership)

    def first_membership_range_date(self):
        start_date = self.created_at
        _, days_in_month = calendar.monthrange(start_date.year,
                                               start_date.month)
        pass_days = start_date.day
        days_left = days_in_month - pass_days
        end_date = start_date + timedelta(days=days_left)
        return start_date, end_date

    @classmethod
    def current_membership(cls, user):
        last_payment = cls.objects.\
            filter(customer__user=user).last()
        start_date = last_payment.created_at
        _, days_in_month = calendar.monthrange(start_date.year,
                                               start_date.month)
        start_date.replace(day=1)
        end_date = start_date + timedelta(days=days_in_month)
        return start_date, end_date

    def get_membership_range_date(self):
        start_date = self.created_at
        _, days_in_month = calendar.monthrange(start_date.year,
                                               start_date.month)
        start_date.replace(day=1)
        end_date = start_date + timedelta(days=days_in_month)
        return start_date, end_date

    @classmethod
    def create(cls, data):
        stripe_charge = data.pop('stripe_charge', None)
        instance = cls.objects.create(**data)
        instance.stripe_charge_id = stripe_charge.id
        instance.last4 = stripe_charge.source.last4
        instance.cc_brand = stripe_charge.source.brand
        instance.save()
        return instance


class BookingPrice(models.Model):
    price_per_day = models.FloatField()
    special_month_price = models.FloatField()


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    free_days = models.IntegerField(default=0)
    final_price = models.FloatField()

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance

    @classmethod
    def get_ramaining_free_days(cls, user, start_date, end_date):

        TWO_DAYS = 2

        start_month = start_date.month
        end_month = end_date.month
        months = abs(start_month - (end_month + 12) if end_month < start_month
                     else end_month - start_month)
        current_date = datetime.today()
        current_month_bookings = cls.objects.filter(bookingorder__customer__user=user,
                                                    start_date__month=current_date.month)
        free_days_this_month = TWO_DAYS - sum(map(lambda x: x.free_days, current_month_bookings))
        total_free_days = months * TWO_DAYS + free_days_this_month
        return total_free_days

    @classmethod
    def booking_price(cls, user, start_date, end_date):

        MAX_MONTH_PRICE = BookingPrice.objects.last().special_month_price
        MAX_MONTH_DAYS_PROMOTION = 31
        MIN_MONTH_DAYS_PROMOTION = 19

        booking_prices = BookingPrice.objects.last()
        price_per_day = booking_prices.price_per_day
        booking_days = (end_date - start_date).days + 1
        months = booking_days // MAX_MONTH_DAYS_PROMOTION
        remanent_days = booking_days % MAX_MONTH_DAYS_PROMOTION
        months_prices = months * MAX_MONTH_PRICE
        remanent_days_price = remanent_days * price_per_day \
            if remanent_days <= MIN_MONTH_DAYS_PROMOTION else MAX_MONTH_PRICE
        normal_price = months_prices + remanent_days_price

        free_days = cls.get_ramaining_free_days(user, start_date, end_date)
        final_booking_price = normal_price - (free_days * price_per_day)

        return normal_price, final_booking_price, free_days


class BookingOrder(Ordereable, models.Model):
    booking = models.OneToOneField(Booking)
    original_price = models.FloatField()
    special_month_price = models.FloatField()

    def booking_days(self):
        return (self.booking.end_date - self.booking.start_date).days + 1


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

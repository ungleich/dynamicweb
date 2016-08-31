
import calendar
from datetime import datetime, date, timedelta
from django.db import models
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

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance


class MembershipOrder(Ordereable, models.Model):
    membership = models.ForeignKey(Membership)

    @classmethod
    def create(cls, data):
        stripe_charge = data.pop('stripe_charge', None)
        instance = cls.objects.create(**data)
        instance.stripe_charge_id = stripe_charge.id
        instance.last4 = stripe_charge.source.last4
        instance.cc_brand = stripe_charge.source.brand
        return instance


class BookingPrice(models.Model):
    price_per_day = models.FloatField()
    special_price_offer = models.FloatField()


class Booking(models.Model):
    start_date = models.DateField()
    end_date = models.DateField()
    price = models.FloatField()
    free_days = models.IntegerField(default=0)

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance

    @classmethod
    def get_ramaining_free_days(cls, user):
        # ZERO_DAYS = 0
        # ONE_DAY = 1
        TWO_DAYS = 2

        current_date = datetime.today()
        current_month_bookings = cls.objects.filter(bookingorder__customer__user=user,
                                                    start_date__month=current_date.month)
        free_days = TWO_DAYS - sum(map(lambda x: x.days, current_month_bookings))
        return free_days

        # free_days = ZERO_DAYS if current_month_bookings.count() > 2 else TWO_DAYS
        # if current_month_bookings.count() == 1:
        #     booking = current_month_bookings.get()
        #     booked_days = (booking.end_date - booking.start_date).days
        #     free_days = ONE_DAY if booked_days == 1 else ZERO_DAYS
        #     return free_days

        # free_days = ZERO_DAYS if current_month_bookings.count() > 2 else TWO_DAYS
        # return free_days

    @classmethod
    def booking_price(cls, user, start_date, end_date):
        """
            Calculate the booking price for requested dates
            How it does:
            1. Check if the user has booked the current month
            2. Get how many days user wants to book
            3. Get price per day from BookingPrices instance
            4. Get available free days
            5. Calculate price by  this formula -> (booking_days - free_days) * price_per_day
        """
        booking_prices = BookingPrice.objects.last()
        price_per_day = booking_prices.price_per_day
        booking_days = (end_date - start_date).days

        free_days = cls.get_ramaining_free_days(user)
        final_booking_price = (booking_days - free_days) * price_per_day
        original_booking_price = (booking_days) * price_per_day

        return original_booking_price, final_booking_price, free_days


class BookingOrder(Ordereable, models.Model):
    booking = models.OneToOneField(Booking)


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

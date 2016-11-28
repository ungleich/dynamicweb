
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

    STANDARD = 'standard'
    MEMBERSHIP_TYPES = (
        (STANDARD, 'Standard'),

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
    start_date = models.DateField()
    end_date = models.DateField()

    @classmethod
    def get_current_membership(cls, user):

        has_order_current_month = Q(membershiporder__customer__user=user,
                                    membershiporder__created_at__month=datetime.today().month)
        # import pdb;pdb.set_trace()
        return cls.objects.\
            filter(has_order_current_month).last()

    # def get_current_active_membership(cls, user):
    #     membership = cls.get_current_membership(user)
    #     return membership if membership and membership.active else None

    @classmethod
    def get_by_user(cls, user):
        return cls.objects.\
            filter(membershiporder__customer__user=user).last()

    @classmethod
    def create(cls, data):
        instance = cls.objects.create(**data)
        return instance

    @classmethod
    def activate_or_crete(cls, data, user):
        membership = cls.get_by_user(user)
        membership_id = membership.id if membership else None
        obj, created = cls.objects.update_or_create(id=membership_id, defaults=data)
        return obj

    @classmethod
    def is_digitalglarus_active_member(cls, user):
        # past_month = (datetime.today() - relativedelta(months=1)).month
        has_order_current_month = Q(membershiporder__customer__user=user,
                                    membershiporder__created_at__month=datetime.today().month)
        # has_order_past_month = Q(membershiporder__customer__user=user,
                                 # membershiporder__created_at__month=past_month)
        active_membership = Q(active=True)
        # return cls.objects.filter(has_order_past_month | has_order_current_month).\
        return cls.objects.filter(has_order_current_month).\
            filter(active_membership).exists()

    def update_dates(self, start_date, end_date):
        self.start_date = start_date
        self.end_date = end_date
        self.save()

    def deactivate(self):
        self.active = False
        self.save()

    def activate(self):
        self.active = True
        self.save()


class MembershipOrder(Ordereable, models.Model):
    membership = models.ForeignKey(Membership)
    start_date = models.DateField()
    end_date = models.DateField()

    @classmethod
    def current_membership_dates(cls, user):
        last_membership_payment = cls.objects.\
            filter(customer__user=user).last()
        if not last_membership_payment:
            return [None, None]

        return last_membership_payment.start_date, last_membership_payment.end_date

    @classmethod
    def next_membership_dates(cls, user):
        current_start_date, current_end_date = cls.current_membership_dates(user)
        if not current_start_date or not current_end_date:
            return [None, None]
        next_start_date = current_end_date + relativedelta(months=1)
        _, days_in_month = calendar.monthrange(next_start_date.year,
                                               next_start_date.month)
        next_start_date = next_start_date.replace(day=1)
        next_end_date = next_start_date + timedelta(days=days_in_month)
        return next_start_date, next_end_date

    def first_membership_range_date(self):
        start_date = self.created_at
        _, days_in_month = calendar.monthrange(start_date.year,
                                               start_date.month)
        pass_days = start_date.day
        days_left = days_in_month - pass_days
        end_date = start_date + timedelta(days=days_left)
        return start_date, end_date

    def get_membership_order_cc_data(self):
        return {
            'last4': self.last4,
            'cc_brand': self.cc_brand,
        }

    def get_membership_range_date(self):
        return self.start_date, self.end_date

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
        ONE_DAY = 1
        start_month = start_date.month
        end_month = end_date.month
        months = abs(start_month - (end_month + 12) if end_month < start_month
                     else end_month - start_month)
        current_date = datetime.today()
        current_month_bookings = cls.objects.filter(bookingorder__customer__user=user,
                                                    start_date__month=current_date.month)
        free_days_this_month = TWO_DAYS - sum(map(lambda x: x.free_days, current_month_bookings))

        if start_date == end_date and free_days_this_month == TWO_DAYS:
            free_days_this_month = ONE_DAY

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

    APPROVED, CANCELLED = range(1, 3)

    STATUS_CHOICES = (
        (APPROVED, 'Approved'),
        (CANCELLED, 'Cancelled')
    )

    booking = models.OneToOneField(Booking)
    original_price = models.FloatField()
    special_month_price = models.FloatField()
    status = models.PositiveIntegerField(choices=STATUS_CHOICES, default=1)

    @classmethod
    def user_has_not_bookings(cls, user):
        return cls.objects.filter(customer__user=user).exists()

    def get_booking_cc_data(self):
        return {
            'last4': self.last4,
            'cc_brand': self.cc_brand,
        } if self.last4 and self.cc_brand else None

    def booking_days(self):
        return (self.booking.end_date - self.booking.start_date).days + 1

    def cancellation_available(self):
        days_to_start = (booking.start_date - datetime.today()).days
        return False if days_to_start < 7 else True


    def cancel(self):
        self.status = self.CANCELLED
        self.save()


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

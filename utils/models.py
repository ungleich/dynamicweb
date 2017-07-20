from django.db import models

from membership.models import CustomUser

from .fields import CountryField


# Create your models here.

class BaseBillingAddress(models.Model):
    cardholder_name = models.CharField(max_length=100, default="")
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = CountryField()

    class Meta:
        abstract = True


class BillingAddress(BaseBillingAddress):
    def __str__(self):
        return self.street_address


class UserBillingAddress(BaseBillingAddress):
    user = models.ForeignKey(CustomUser, related_name='billing_addresses')
    current = models.BooleanField(default=True)

    def __str__(self):
        return self.street_address

    def to_dict(self):
        return {
            'Cardholder Name': self.cardholder_name,
            'Street Address': self.street_address,
            'City': self.city,
            'Postal Code': self.postal_code,
            'Country': self.country,
        }


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200, blank=True)
    message = models.TextField()
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "%s - %s - %s" % (self.name, self.email, self.received_date)

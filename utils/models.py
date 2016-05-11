from django.db import models

from .fields import CountryField

# Create your models here.


class BillingAddress(models.Model):
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length=50)
    postal_code = models.CharField(max_length=50)
    country = CountryField()

    def __str__(self):
        """
        str cast with a friendly representation of the BillingAddress object
        """
        return "%s %s %s %s" % (self.street_address, self.city, self.postal_code, self.country)


class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=200)
    message = models.TextField()
    received_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        """
        str cast with a friendly representation of the ContactMessage object
        """
        return "%s - %s - %s" % (self.name, self.email, self.received_date)

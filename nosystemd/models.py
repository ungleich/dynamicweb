from django.db import models
from membership.models import CustomUser
from utils.models import BillingAddress


# Create your models here.


class Donation(models.Model):

    donation = models.FloatField()
    donator = models.ForeignKey(CustomUser)
    created_at = models.DateTimeField(auto_now_add=True)
    billing_address = models.ForeignKey(BillingAddress)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)

    @classmethod
    def create(cls, data):
        obj = cls.objects.create(**data)
        return obj

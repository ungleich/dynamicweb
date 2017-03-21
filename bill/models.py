from django.db import models
from utils.models import BillingAddress
from membership.models import CustomUser


class Customer(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = BillingAddress
    rate = models.FloatField

class Item(models.Model):
    description = models.TextField
    # Netto, brutto price is calced via Bill.mwst_percent
    price = models.FloatField


class Bill(models.Model):
    customer = models.ForeignKey(Customer)
    items = models.ForeignKey(Item)
    date = models.DateField()
    mwst_percent = models.FloatField
    # TODO: We could calc these things on the fly
    mwst = models.FloatField
    netto = models.FloatField
    brutto = models.FloatField



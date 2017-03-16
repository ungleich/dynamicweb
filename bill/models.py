from django.db import models
from utils.models import BillingAddress

class Bill(models.Model):
    customer = models.ForeignKey(Customer)
    items = models.ForeignKey(Item)
    date = model.DateField()
    mwst_percent = model.FloatField
    # TODO: We could calc these things on the fly
    mwst = model.FloatField
    netto = model.FloatField
    brutto = model.FloatField

class Customer(model.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = BillingAddress
    rate = model.FloatField

class Item(model.Model):
    description = model.TextField
    # Netto, brruto price is calced via Bill.mwst_percent
    price = model.FloatField


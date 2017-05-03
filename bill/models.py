from django.db import models
from utils.models import BillingAddress
from membership.models import CustomUser


class Customer(models.Model):
    user_id = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    address = models.ForeignKey(BillingAddress)
    rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.user_id.email


class Bill(models.Model):
    customer = models.ForeignKey(Customer)
    date = models.DateField()
    mwst_percent = models.FloatField(default=1.08)
    # TODO: We could calc these things on the fly
    mwst = models.FloatField(default=0.0)
    netto = models.FloatField(default=0.0)
    brutto = models.FloatField(default=0.0)

    def __str__(self):
        return "Bill for customer: {}".format(self.customer)

    def prepare(self):
        # Reset Bill
        self.mwst = 0.0
        self.netto = 0.0
        self.brutto = 0.0
        for item in self.item_set.all():
            self.brutto += item.price
        self.netto = self.brutto * self.mwst_percent
        self.mwst = self.netto - self.brutto
        self.save()

class Item(models.Model):
    description = models.TextField(default="")
    # Brutto
    price = models.FloatField(default=0.0)
    # Many to Many relationship with bills 
    bills = models.ManyToManyField(Bill)

    def __str__(self):
        return self.description



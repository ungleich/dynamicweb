import os
import socket
import logging


import oca
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from hosting.opennebula_functions import OpenNebulaManager

from django.conf import settings

from Crypto.PublicKey import RSA
from stored_messages.settings import stored_messages_settings

from membership.models import StripeCustomer, CustomUser
from utils.models import BillingAddress
from utils.mixins import AssignPermissionsMixin
from .managers import VMPlansManager
from oca.exceptions import OpenNebulaException
from oca.pool import WrongNameError

logger = logging.getLogger(__name__)


class HostingOrder(AssignPermissionsMixin, models.Model):

    ORDER_APPROVED_STATUS = 'Approved'
    ORDER_DECLINED_STATUS = 'Declined'

    vm_id = models.IntegerField(default=0)
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)
    price = models.FloatField()

    permissions = ('view_hostingorder',)

    class Meta:
        permissions = (
            ('view_hostingorder', 'View Hosting Order'),
        )

    def __str__(self):
        return "%s" % (self.id)

    @cached_property
    def status(self):
        return self.ORDER_APPROVED_STATUS if self.approved else self.ORDER_DECLINED_STATUS

    @classmethod
    def create(cls, price=None, vm_id=None, customer=None, billing_address=None):
        instance = cls.objects.create(
            price=price,
            vm_id=vm_id,
            customer=customer,
            billing_address=billing_address
        )
        instance.assign_permissions(customer.user)
        return instance

    def set_approved(self):
        self.approved = True
        self.save()

    def set_stripe_charge(self, stripe_charge):
        self.stripe_charge_id = stripe_charge.id
        self.last4 = stripe_charge.source.last4
        self.cc_brand = stripe_charge.source.brand
        self.save()

    def get_cc_data(self):
        return {
            'last4': self.last4,
            'cc_brand': self.cc_brand,
        } if self.last4 and self.cc_brand else None


class UserHostingKey(models.Model):
    user = models.ForeignKey(CustomUser)
    public_key = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=100)

    @staticmethod
    def generate_RSA(bits=2048):
        '''
        Generate an RSA keypair with an exponent of 65537 in PEM format
        param: bits The key length in bits
        Return private key and public key
        '''
        new_key = RSA.generate(2048, os.urandom)
        public_key = new_key.publickey().exportKey("OpenSSH")
        private_key = new_key.exportKey("PEM")
        return private_key, public_key

    @classmethod
    def generate_keys(cls):
        private_key, public_key = cls.generate_RSA()
        # self.public_key = public_key
        # self.save(update_fields=['public_key'])
        return private_key, public_key

class HostingBill(AssignPermissionsMixin, models.Model):
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    total_price = models.FloatField(default=0.0)

    permissions = ('view_hostingbill',)

    class Meta:
        permissions = (
            ('view_hostingbill', 'View Hosting Bill'),
        )

    def __str__(self):
        return "%s" % (self.customer.user.email)

    @classmethod
    def create(cls, customer=None, billing_address=None):
        instance = cls.objects.create(customer=customer, billing_address=billing_address)
        return instance


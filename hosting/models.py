import os
import logging

from django.db import models
from django.utils.functional import cached_property
from Crypto.PublicKey import RSA
from membership.models import StripeCustomer, CustomUser
from utils.models import BillingAddress
from utils.mixins import AssignPermissionsMixin

logger = logging.getLogger(__name__)


class HostingPlan(models.Model):
    disk_size = models.FloatField(default=0.0)
    cpu_cores = models.FloatField(default=0.0)
    memory = models.FloatField(default=0.0)

    def serialize(self):
        return {
            'id': self.id,
            'cpu': self.cpu_cores,
            'memory': self.memory,
            'disk_size': self.disk_size,
            'price': self.price(),
        }

    @classmethod
    def get_serialized_configs(cls):
        return [cfg.serialize()
                for cfg in cls.objects.all()]

    def price(self):
        price = self.disk_size * 0.6
        price += self.cpu_cores * 5
        price += self.memory * 2
        return price


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
    subscription_id = models.CharField(max_length=100, null=True)

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
    def create(cls, price=None, vm_id=None, customer=None,
               billing_address=None):
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

    def set_subscription_id(self, subscription_object, cc_details):
        """
        When creating a Stripe subscription, we have subscription id.
        We store this in the subscription_id field.
        This method sets the subscription id from subscription_object
        and also the last4 and credit card brands used for this order.

        :param subscription_object: Stripe's subscription object
        :param cc_details: A dict containing card details
        {last4, brand}
        :return:
        """
        self.subscription_id = subscription_object.id
        self.last4 = cc_details.get('last4')
        self.cc_brand = cc_details.get('brand')
        self.save()

    def get_cc_data(self):
        return {
            'last4': self.last4,
            'cc_brand': self.cc_brand,
        } if self.last4 and self.cc_brand else None


class UserHostingKey(models.Model):
    user = models.ForeignKey(CustomUser)
    public_key = models.TextField()
    private_key = models.FileField(upload_to='private_keys', blank=True)
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
        instance = cls.objects.create(customer=customer,
                                      billing_address=billing_address)
        return instance

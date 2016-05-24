import os

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property
from membership.models import StripeCustomer
from utils.models import BillingAddress

from Crypto.PublicKey import RSA


from .managers import VMPlansManager


class VirtualMachineType(models.Model):

    HETZNER_NUG = 'hetzner_nug'
    HETZNER = 'hetzner'
    HETZNER_R6 = 'hetzner_raid6'
    HETZNER_G = 'hetzner_glusterfs'
    BERN = 'bern'
    DE_LOCATION = 'DE'
    CH_LOCATION = 'CH'

    HOSTING_TYPES = (
        (HETZNER_NUG, 'Hetzner No Uptime Guarantee'),
        (HETZNER, 'Hetzner'),
        (HETZNER_R6, 'Hetzner Raid6'),
        (HETZNER_G, 'Hetzner Glusterfs'),
        (BERN, 'Bern'),
    )

    LOCATIONS_CHOICES = (
        (DE_LOCATION, 'Germany'),
        (CH_LOCATION, 'Switzerland'),
    )
    description = models.TextField()
    base_price = models.FloatField()
    memory_price = models.FloatField()
    core_price = models.FloatField()
    disk_size_price = models.FloatField()
    hosting_company = models.CharField(max_length=30, choices=HOSTING_TYPES)
    location = models.CharField(max_length=3, choices=LOCATIONS_CHOICES)

    def __str__(self):
        return "%s" % (self.get_hosting_company_display())

    @classmethod
    def get_serialized_vm_types(cls):
        return [vm.get_serialized_data()
                for vm in cls.objects.all()]

    def calculate_price(self, specifications):
        price = float(specifications['cores']) * self.core_price
        price += float(specifications['memory']) * self.memory_price
        price += float(specifications['disk_size']) * self.disk_size_price
        price += self.base_price
        return price

    def defeault_price(self):
        price = self.base_price
        price += self.core_price
        price += self.memory_price
        price += self.disk_size_price * 10
        return price

    def get_serialized_data(self):
        return {
            'description': self.description,
            'base_price': self.base_price,
            'core_price': self.core_price,
            'disk_size_price': self.disk_size_price,
            'memory_price': self.memory_price,
            'hosting_company_name': self.get_hosting_company_display(),
            'hosting_company': self.hosting_company,
            'default_price': self.defeault_price(),
            'location_code': self.location,
            'location': self.get_location_display(),
            'id': self.id,
        }


class VirtualMachinePlan(models.Model):
    cores = models.IntegerField()
    memory = models.IntegerField()
    disk_size = models.IntegerField()
    vm_type = models.ForeignKey(VirtualMachineType)
    price = models.FloatField()
    public_key = models.TextField()

    objects = VMPlansManager()

    def __str__(self):
        return "%s" % (self.id)

    @cached_property
    def hosting_company_name(self):
        return self.vm_type.get_hosting_company_display()

    @cached_property
    def name(self):
        name = 'vm-%s' % self.id
        return name

    @classmethod
    def create(cls, data, user):
        instance = cls.objects.create(**data)
        return instance

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

    def generate_keys(self):
        private_key, public_key = self.generate_RSA()
        self.public_key = public_key
        self.save(update_fields=['public_key'])
        return private_key


class HostingOrder(models.Model):

    ORDER_APPROVED_STATUS = 'Approved'
    ORDER_DECLINED_STATUS = 'Declined'

    vm_plan = models.ForeignKey(VirtualMachinePlan, related_name='hosting_orders')
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=10)
    stripe_charge_id = models.CharField(max_length=100, null=True)

    def __str__(self):
        return "%s" % (self.id)

    @cached_property
    def status(self):
        return self.ORDER_APPROVED_STATUS if self.approved else self.ORDER_DECLINED_STATUS

    @classmethod
    def create(cls, vm_plan=None, customer=None, billing_address=None):
        instance = cls.objects.create(vm_plan=vm_plan, customer=customer,
                                      billing_address=billing_address)
        return instance

    def set_approved(self):
        self.approved = True
        self.save()

    def set_stripe_charge(self, stripe_charge):
        self.stripe_charge_id = stripe_charge.id
        self.last4 = stripe_charge.source.last4
        self.cc_brand = stripe_charge.source.brand
        self.save()













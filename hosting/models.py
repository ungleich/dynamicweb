import os

import oca
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from Crypto.PublicKey import RSA
from stored_messages.settings import stored_messages_settings

from membership.models import StripeCustomer
from utils.models import BillingAddress
from utils.mixins import AssignPermissionsMixin
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


class VirtualMachinePlan(AssignPermissionsMixin, models.Model):

    PENDING_STATUS = 'pending'
    ONLINE_STATUS = 'online'
    CANCELED_STATUS = 'canceled'

    VM_STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending for activation'),
        (ONLINE_STATUS, 'Online'),
        (CANCELED_STATUS, 'Canceled')
    )

    DJANGO = 'django'
    RAILS = 'rails'
    NODEJS = 'nodejs'

    VM_CONFIGURATION = (
        (DJANGO, 'Ubuntu 14.04, Django'),
        (RAILS, 'Ubuntu 14.04, Rails'),
        (NODEJS, 'Debian, NodeJS'),
    )

    permissions = ('view_virtualmachineplan',
                   'cancel_virtualmachineplan',
                   'change_virtualmachineplan')

    cores = models.IntegerField()
    memory = models.IntegerField()
    disk_size = models.IntegerField()
    vm_type = models.ForeignKey(VirtualMachineType)
    price = models.FloatField()
    public_key = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=VM_STATUS_CHOICES, default=PENDING_STATUS)
    ip = models.CharField(max_length=50, blank=True)
    configuration = models.CharField(max_length=20, choices=VM_CONFIGURATION)

    objects = VMPlansManager()

    class Meta:
        permissions = (
            ('view_virtualmachineplan', 'View Virtual Machine Plan'),
            ('cancel_virtualmachineplan', 'Cancel Virtual Machine Plan'),
        )

    def __str__(self):
        return self.name

    @cached_property
    def hosting_company_name(self):
        return self.vm_type.get_hosting_company_display()

    @cached_property
    def location(self):
        return self.vm_type.get_location_display()

    @cached_property
    def name(self):
        name = 'vm-%s' % self.id
        return name

    @cached_property
    def notifications(self):
        stripe_customer = StripeCustomer.objects.get(hostingorder__vm_plan=self)
        backend = stored_messages_settings.STORAGE_BACKEND()
        messages = backend.inbox_list(stripe_customer.user)
        return messages

    @classmethod
    def create(cls, data, user):
        instance = cls.objects.create(**data)
        instance.assign_permissions(user)
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
        return private_key, public_key

    def cancel_plan(self):
        self.status = self.CANCELED_STATUS
        self.save(update_fields=['status'])


class HostingOrder(AssignPermissionsMixin, models.Model):

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
    def create(cls, vm_plan=None, customer=None, billing_address=None):
        instance = cls.objects.create(vm_plan=vm_plan, customer=customer,
                                      billing_address=billing_address)
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


class ManageVM(models.Model):
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False

    class Meta:
        managed = False

class HostingBill(AssignPermissionsMixin, models.Model):
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)

    permissions = ('view_hostingbill',)

    class Meta:
        permissions = (
            ('view_hostingbill', 'View Hosting Bill'),
        )

    def __str__(self):
        return "%s" % (self.customer.user.email)


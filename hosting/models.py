import os
import socket

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

import logging
logger = logging.getLogger(__name__)

class VirtualMachineType(models.Model):

    description = models.TextField()
    base_price = models.FloatField()
    memory_price = models.FloatField()
    core_price = models.FloatField()
    disk_size_price = models.FloatField()
    cores = models.IntegerField()
    memory = models.IntegerField()
    disk_size = models.IntegerField()

    def __str__(self):
        return "VM Type %s" % (self.id)

    @cached_property
    def final_price(self):
        price = self.cores * self.core_price
        price += self.memory * self.memory_price
        price += self.disk_size * self.disk_size_price
        return price

    @classmethod
    def get_serialized_vm_types(cls):
        return [vm.get_serialized_data()
                for vm in cls.objects.all()]

    def calculate_price(self):
        price = self.cores * self.core_price
        price += self.memory * self.memory_price
        price += self.disk_size * self.disk_size_price
        # price += self.base_price
        return price

    # @classmethod
    # def get_price(cls, vm_template):
    #     return cls.BASE_PRICE * vm_template

    def get_specs(self):
        return {
            'memory': self.memory,
            'cores': self.cores,
            'disk_size': self.disk_size
        }

    # def calculate_price(self, vm_template):
    #     price = self.base_price * vm_template
    #     return price

    # def defeault_price(self):
    #     price = self.base_price
    #     price += self.core_price
    #     price += self.memory_price
    #     price += self.disk_size_price * 10
    #     return price

    def get_serialized_data(self):
        return {
            'description': self.description,
            'core_price': self.core_price,
            'disk_size_price': self.disk_size_price,
            'memory_price': self.memory_price,
            'id': self.id,
            'final_price': self.final_price,
            'cores': self.cores,
            'memory': self.memory,
            'disk_size': self.disk_size

        }

    @classmethod
    def get_vm_templates(self, user):
        opennebula_client = OpenNebulaManager(
            email=user.email,
            password=user.password,
        )

        templates = opennebula_client.get_vm_templates()
        for template in templates:
            print(OpenNebulaManager.parse_vm(template))
        return templates


class VirtualMachinePlan(AssignPermissionsMixin, models.Model):

    PENDING_STATUS = 'pending'
    ONLINE_STATUS = 'online'
    CANCELED_STATUS = 'canceled'

    VM_STATUS_CHOICES = (
        (PENDING_STATUS, 'Pending for activation'),
        (ONLINE_STATUS, 'Online'),
        (CANCELED_STATUS, 'Canceled')
    )

    # DJANGO = 'django'
    # RAILS = 'rails'
    # NODEJS = 'nodejs'

    # VM_CONFIGURATION = (
    #     (DJANGO, 'Ubuntu 14.04, Django'),
    #     (RAILS, 'Ubuntu 14.04, Rails'),
    #     (NODEJS, 'Debian, NodeJS'),
    # )

    VM_CONFIGURATION = (
        ('debian', 'Debian 8'),
        ('ubuntu', 'Ubuntu 16.06'),
        ('devuan', 'Devuan 1'),
        ('centos', 'CentOS 7')
    )

    permissions = ('view_virtualmachineplan',
                   'cancel_virtualmachineplan',
                   'change_virtualmachineplan')

    cores = models.IntegerField()
    memory = models.IntegerField()
    disk_size = models.IntegerField()
    vm_type = models.ForeignKey(VirtualMachineType, null=True)
    price = models.FloatField()
    public_key = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=VM_STATUS_CHOICES, default=PENDING_STATUS)
    ip = models.CharField(max_length=50, blank=True)
    configuration = models.CharField(max_length=20, choices=VM_CONFIGURATION)
    opennebula_id = models.IntegerField(null=True)

    objects = VMPlansManager()

    class Meta:
        permissions = (
            ('view_virtualmachineplan', 'View Virtual Machine Plan'),
            ('cancel_virtualmachineplan', 'Cancel Virtual Machine Plan'),
        )

    def __str__(self):
        return self.name

    # @cached_property
    # def hosting_company_name(self):
    #     return self.vm_type.get_hosting_company_display()

    # @cached_property
    # def location(self):
    #     return self.vm_type.get_location_display()

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

    def cancel_plan(self, vm_id):
        self.status = self.CANCELED_STATUS
        self.save(update_fields=['status'])

    @classmethod
    def terminate_opennebula_vm(self, user, vm_id):

        opennebula_client = OpenNebulaManager(
            user.email,
            user.password,
        )

        return opennebula_client.terminate_vm(vm_id)


    @classmethod
    def create_opennebula_vm(self, user, specs):
        # import pdb
        # pdb.set_trace()


        # Init opennebula manager using given user
        opennebula_client = OpenNebulaManager(
            user.email,
            user.password,
        )

        # Create a vm in opennebula using given specs
        vm = opennebula_client.create_vm(specs)
        return vm

    @classmethod
    def get_vm(self, user, vm_id):
        # Get opennebula client
        opennebula_client = OpenNebulaManager(
            email=user.email,
            password=user.password,
        )

        # Get vm given the id
        vm = opennebula_client.get_vm(
            user.email,
            vm_id
        )

        # Parse vm data
        vm_data = OpenNebulaManager.parse_vm(vm)

        return vm_data

    @classmethod
    def get_vms(self, user):

        # Get opennebula client
        opennebula_client = OpenNebulaManager(
            email=user.email,
            password=user.password,
        )

        # Get vm pool
        vm_pool = opennebula_client.get_vms(user.email)

        # Reset total price
        self.total_price = 0
        vms = []
        # Add vm in vm_pool to context
        for vm in vm_pool:
            vm_data = OpenNebulaManager.parse_vm(vm)
            vms.append(vm_data)
            # self.total_price += price
        # self.save()
        return vms


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

    def get_vms(self):
        email = self.customer.user.email
        # Get opennebula client
        opennebula_client = OpenNebulaManager(create_user=False)

        # Get vm pool
        vm_pool = opennebula_client.get_vms(email)

        # Reset total price
        self.total_price = 0
        vms = []
        # Add vm in vm_pool to context
        for vm in vm_pool:
            vm_data = OpenNebulaManager.parse_vm(vm)
            self.total_price += vm_data['price']
            vms.append(vm_data)
        self.save()
        return vms


        
def get_user_opennebula_password():
    '''
    TODO: Implement the way we obtain the user's opennebula password 
    '''
    pw = os.environ.get('OPENNEBULA_USER_PW')
    if pw is None:
        raise Exception("Define OPENNEBULA_USER_PW env variable")
    return pw

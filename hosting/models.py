import os
import oca

from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.utils.functional import cached_property

from django.conf import settings

from Crypto.PublicKey import RSA
from stored_messages.settings import stored_messages_settings

from membership.models import StripeCustomer, CustomUser
from utils.models import BillingAddress
from utils.mixins import AssignPermissionsMixin
from .managers import VMPlansManager
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

    def cancel_plan(self):
        self.status = self.CANCELED_STATUS
        self.save(update_fields=['status'])

    @classmethod
    def get_vms(self, email):
        # Get User
        user_email = email

        # Connect to open nebula server
        # TODO: handle potential connection error
        oneadmin_client = oca.Client("{0}:{1}".format(
            settings.OPENNEBULA_USERNAME,
            settings.OPENNEBULA_PASSWORD),
            "{protocol}://{domain}:{port}{endpoint}".format(
                protocol=settings.OPENNEBULA_PROTOCOL,
                domain=settings.OPENNEBULA_DOMAIN,
                port=settings.OPENNEBULA_PORT,
                endpoint=settings.OPENNEBULA_ENDPOINT
        ))
        # Get open nebula user id for given email
        user_pool = oca.UserPool(oneadmin_client)
        user_pool.info()
        try:
            user = user_pool.get_by_name(user_email)
            user_id = user.id
            logger.debug("User {user} exists.".format(user=user_email))
        except WrongNameError as wrong_name_err:
            # User does not exist. So, we create this user in OpenNebula
            password = get_user_opennebula_password()
            # We use the core authenticator driver for the new user
            user_id = oneadmin_client.call('user.allocate', 
                                           user_email, password,
                                           'core')
            logger.debug("User {0} does not exist. Created the user. User id = {1}", user_email, user_id)
            
        # We should now have an OpenNebula user corresponding to user_email
        # It is now ok to now perform opennebula functions with this user's client
        client = oca.Client("{0}:{1}".format(
            user_email,
            get_user_opennebula_password()),
            "{protocol}://{domain}:{port}{endpoint}".format(
                protocol=settings.OPENNEBULA_PROTOCOL,
                domain=settings.OPENNEBULA_DOMAIN,
                port=settings.OPENNEBULA_PORT,
                endpoint=settings.OPENNEBULA_ENDPOINT
        ))

        # Get vm_pool for given user_id
        vm_pool = oca.VirtualMachinePool(client)
        vm_pool.info(filter=user_id)

        # Reset total price
        self.total_price = 0
        vms = []
        # Add vm in vm_pool to context
        for vm in vm_pool:
            name = vm.name
            cores = int(vm.template.vcpu)
            memory = int(vm.template.memory) / 1024
            # Check if vm has more than one disk
            if 'DISK' in vm.template.multiple:
                disk_size = 0
                for disk in vm.template.disks:
                    disk_size += int(disk.size) / 1024
            else:
                disk_size = int(vm.template.disk.size) / 1024

            #TODO: Replace with vm plan
            price = 0.6 * disk_size + 2 * memory + 5 * cores
            vm = {}
            vm['name'] = name
            vm['price'] = price
            vm['disk_size'] = disk_size
            vm['cores'] = cores
            vm['memory'] = memory
            vms.append(vm)
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
        
def get_user_opennebula_password():
    '''
    TODO: Implement the way we obtain the user's opennebula password 
    '''
    pw = os.environ.get('OPENNEBULA_USER_PW')
    if pw is None:
        raise Exception("Define OPENNEBULA_USER_PW env variable")
    return pw

import logging
import os

from Crypto.PublicKey import RSA
from dateutil.relativedelta import relativedelta
from django.db import models
from django.utils import timezone
from django.utils.functional import cached_property

from datacenterlight.models import VMPricing, VMTemplate
from membership.models import StripeCustomer, CustomUser
from utils.models import BillingAddress
from utils.mixins import AssignPermissionsMixin
from utils.stripe_utils import StripeUtils

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


class OrderDetail(AssignPermissionsMixin, models.Model):
    vm_template = models.ForeignKey(
        VMTemplate, blank=True, null=True, default=None,
        on_delete=models.SET_NULL
    )
    cores = models.IntegerField(default=0)
    memory = models.IntegerField(default=0)
    hdd_size = models.IntegerField(default=0)
    ssd_size = models.IntegerField(default=0)

    def __str__(self):
        return "Not available" if self.vm_template is None else (
            "%s - %s, %s cores, %s GB RAM, %s GB SSD" % (
                self.vm_template.name, self.vm_template.vm_type, self.cores,
                self.memory, self.ssd_size
            )
        )


class HostingOrder(AssignPermissionsMixin, models.Model):
    ORDER_APPROVED_STATUS = 'Approved'
    ORDER_DECLINED_STATUS = 'Declined'

    vm_id = models.IntegerField(default=0)
    customer = models.ForeignKey(StripeCustomer)
    billing_address = models.ForeignKey(BillingAddress)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)
    last4 = models.CharField(max_length=4)
    cc_brand = models.CharField(max_length=128)
    stripe_charge_id = models.CharField(max_length=100, null=True)
    price = models.FloatField()
    subscription_id = models.CharField(max_length=100, null=True)
    vm_pricing = models.ForeignKey(VMPricing)
    order_detail = models.ForeignKey(
        OrderDetail, null=True, blank=True, default=None,
        on_delete=models.SET_NULL
    )

    permissions = ('view_hostingorder',)

    class Meta:
        permissions = (
            ('view_hostingorder', 'View Hosting Order'),
        )

    def __str__(self):
        return ("Order Nr: #{} - VM_ID: {} - {} - {} - "
                "Specs: {} - Price: {}").format(
            self.id, self.vm_id, self.customer.user.email, self.created_at,
            self.order_detail, self.price
        )

    @cached_property
    def status(self):
        return self.ORDER_APPROVED_STATUS if self.approved else self.ORDER_DECLINED_STATUS

    @classmethod
    def create(cls, price=None, vm_id=0, customer=None,
               billing_address=None, vm_pricing=None):
        instance = cls.objects.create(
            price=price,
            vm_id=vm_id,
            customer=customer,
            billing_address=billing_address,
            vm_pricing=vm_pricing
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

    def set_subscription_id(self, subscription_id, cc_details):
        """
        When creating a Stripe subscription, we have subscription id.
        We store this in the subscription_id field.
        This method sets the subscription id
        and the last4 and credit card brands used for this order.

        :param subscription_id: Stripe's subscription id
        :param cc_details: A dict containing card details
        {last4, brand}
        :return:
        """
        self.subscription_id = subscription_id
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


class VMDetail(models.Model):
    user = models.ForeignKey(CustomUser)
    vm_id = models.IntegerField(default=0)
    disk_size = models.FloatField(default=0.0)
    cores = models.FloatField(default=0.0)
    memory = models.FloatField(default=0.0)
    configuration = models.CharField(default='', max_length=25)
    ipv4 = models.TextField(default='')
    ipv6 = models.TextField(default='')
    created_at = models.DateTimeField(auto_now_add=True)
    terminated_at = models.DateTimeField(null=True)

    def end_date(self):
        end_date = self.terminated_at if self.terminated_at else timezone.now()
        months = relativedelta(end_date, self.created_at).months or 1
        end_date = self.created_at + relativedelta(months=months, days=-1)
        return end_date


class UserCardDetail(AssignPermissionsMixin, models.Model):
    permissions = ('view_usercarddetail',)
    stripe_customer = models.ForeignKey(StripeCustomer)
    last4 = models.CharField(max_length=4)
    brand = models.CharField(max_length=128)
    card_id = models.CharField(max_length=100, blank=True, default='')
    fingerprint = models.CharField(max_length=100)
    exp_month = models.IntegerField(null=False)
    exp_year = models.IntegerField(null=False)
    preferred = models.BooleanField(default=False)

    class Meta:
        permissions = (
            ('view_usercarddetail', 'View User Card'),
        )

    @classmethod
    def create(cls, stripe_customer=None, last4=None, brand=None,
               fingerprint=None, exp_month=None, exp_year=None, card_id=None,
               preferred=False):
        instance = cls.objects.create(
            stripe_customer=stripe_customer, last4=last4, brand=brand,
            fingerprint=fingerprint, exp_month=exp_month, exp_year=exp_year,
            card_id=card_id, preferred=preferred
        )
        instance.assign_permissions(stripe_customer.user)
        return instance

    @classmethod
    def get_all_cards_list(cls, stripe_customer):
        """
        Get all the cards of the given customer as a list

        :param stripe_customer: The StripeCustomer object
        :return: A list of all cards; an empty list if the customer object is
                 None
        """
        cards_list = []
        if stripe_customer is None:
            return cards_list
        user_card_details = UserCardDetail.objects.filter(
            stripe_customer_id=stripe_customer.id
        ).order_by('-preferred', 'id')
        for card in user_card_details:
            cards_list.append({
                'last4': card.last4, 'brand': card.brand, 'id': card.id,
                'preferred': card.preferred
            })
        return cards_list

    @classmethod
    def get_or_create_user_card_detail(cls, stripe_customer, card_details):
        """
        A method that checks if a UserCardDetail object exists already
        based upon the given card_details and creates it for the given
        customer if it does not exist. It returns the UserCardDetail object
        matching the given card_details if it exists.

        :param stripe_customer: The given StripeCustomer object to whom the
                card object should belong to
        :param card_details: A dictionary identifying a given card
        :return: UserCardDetail object
        """
        try:
            if ('fingerprint' in card_details and 'exp_month' in card_details
                    and 'exp_year' in card_details):
                card_detail = UserCardDetail.objects.get(
                    stripe_customer=stripe_customer,
                    fingerprint=card_details['fingerprint'],
                    exp_month=card_details['exp_month'],
                    exp_year=card_details['exp_year']
                )
            else:
                raise UserCardDetail.DoesNotExist()
        except UserCardDetail.DoesNotExist:
            preferred = False
            if 'preferred' in card_details:
                preferred = card_details['preferred']
            card_detail = UserCardDetail.create(
                stripe_customer=stripe_customer,
                last4=card_details['last4'],
                brand=card_details['brand'],
                fingerprint=card_details['fingerprint'],
                exp_month=card_details['exp_month'],
                exp_year=card_details['exp_year'],
                card_id=card_details['card_id'],
                preferred=preferred
            )
        return card_detail

    @staticmethod
    def set_default_card(stripe_api_cus_id, stripe_source_id):
        """
        Sets the given stripe source as the default source for the given
        Stripe customer
        :param stripe_api_cus_id: Stripe customer id
        :param stripe_source_id: The Stripe source id
        :return:
        """
        stripe_utils = StripeUtils()
        cus_response = stripe_utils.get_customer(stripe_api_cus_id)
        cu = cus_response['response_object']
        cu.default_source = stripe_source_id
        cu.save()
        UserCardDetail.save_default_card_local(
            stripe_api_cus_id, stripe_source_id
        )

    @staticmethod
    def set_default_card_from_stripe(stripe_api_cus_id):
        stripe_utils = StripeUtils()
        cus_response = stripe_utils.get_customer(stripe_api_cus_id)
        cu = cus_response['response_object']
        default_source = cu.default_source
        if default_source is not None:
            UserCardDetail.save_default_card_local(
                stripe_api_cus_id, default_source
            )

    @staticmethod
    def save_default_card_local(stripe_api_cus_id, card_id):
        stripe_cust = StripeCustomer.objects.get(stripe_id=stripe_api_cus_id)
        user_card_detail = UserCardDetail.objects.get(
            stripe_customer=stripe_cust, card_id=card_id
        )
        for card in stripe_cust.usercarddetail_set.all():
            card.preferred = False
            card.save()
        user_card_detail.preferred = True
        user_card_detail.save()

    @staticmethod
    def get_user_card_details(stripe_customer, card_details):
        """
        A utility function to check whether a StripeCustomer is already
        associated with the card having given details

        :param stripe_customer:
        :param card_details:
        :return: The UserCardDetails object if it exists, None otherwise
        """
        try:
            ucd = UserCardDetail.objects.get(
                stripe_customer=stripe_customer,
                fingerprint=card_details['fingerprint'],
                exp_month=card_details['exp_month'],
                exp_year=card_details['exp_year']
            )
            return ucd
        except UserCardDetail.DoesNotExist:
            return None

import logging

from django.db import models

logger = logging.getLogger(__name__)


class VMTemplate(models.Model):
    PUBLIC = 'public'
    IPV6 = 'ipv6only'
    VM_TYPE_CHOICES = (
        (PUBLIC, PUBLIC.title()),
        (IPV6, IPV6.title()),
    )
    name = models.CharField(max_length=50)
    opennebula_vm_template_id = models.IntegerField()
    vm_type = models.CharField(
        max_length=50, choices=VM_TYPE_CHOICES, default=PUBLIC
    )

    def __str__(self):
        return '%s - %s - %s' % (
            self.opennebula_vm_template_id, self.vm_type, self.name
        )

    @classmethod
    def create(cls, name, opennebula_vm_template_id, vm_type):
        vm_template = cls(
            name=name, opennebula_vm_template_id=opennebula_vm_template_id,
            vm_type=vm_type
        )
        return vm_template


class VMPricing(models.Model):
    name = models.CharField(max_length=255, unique=True)
    vat_inclusive = models.BooleanField(default=True)
    vat_percentage = models.DecimalField(
        max_digits=7, decimal_places=5, blank=True, default=0
    )
    cores_unit_price = models.DecimalField(
        max_digits=7, decimal_places=5, default=0
    )
    ram_unit_price = models.DecimalField(
        max_digits=7, decimal_places=5, default=0
    )
    ssd_unit_price = models.DecimalField(
        max_digits=7, decimal_places=5, default=0
    )
    hdd_unit_price = models.DecimalField(
        max_digits=7, decimal_places=6, default=0
    )
    discount_name = models.CharField(max_length=255, null=True, blank=True)
    discount_amount = models.DecimalField(
        max_digits=6, decimal_places=2, default=0
    )

    def __str__(self):
        display_str = self.name + ' => ' + ' - '.join([
            '{}/Core'.format(self.cores_unit_price.normalize()),
            '{}/GB RAM'.format(self.ram_unit_price.normalize()),
            '{}/GB SSD'.format(self.ssd_unit_price.normalize()),
            '{}/GB HDD'.format(self.hdd_unit_price.normalize()),
            '{}% VAT'.format(self.vat_percentage.normalize())
            if not self.vat_inclusive else 'VAT-Incl',
        ])
        if self.discount_amount:
            display_str = ' - '.join([
                display_str,
                '{} {}'.format(
                    self.discount_amount,
                    self.discount_name if self.discount_name else 'Discount'
                )
            ])
        return display_str

    @classmethod
    def get_vm_pricing_by_name(cls, name):
        try:
            pricing = VMPricing.objects.get(name=name)
        except Exception as e:
            logger.error(
                "Error getting VMPricing with name {name}. "
                "Details: {details}. Attempting to return default"
                "pricing.".format(name=name, details=str(e))
            )
            pricing = VMPricing.get_default_pricing()
        return pricing

    @classmethod
    def get_default_pricing(cls):
        """ Returns the default pricing or None """
        try:
            default_pricing = VMPricing.objects.get(name='default')
        except Exception as e:
            logger.error(str(e))
            default_pricing = None
        return default_pricing


class StripePlan(models.Model):
    """
    A model to store Data Center Light's created Stripe plans
    """
    stripe_plan_id = models.CharField(max_length=256, null=True)

    @classmethod
    def create(cls, stripe_plan_id):
        stripe_plan = cls(stripe_plan_id=stripe_plan_id)
        return stripe_plan


class ContactUs(models.Model):
    name = models.CharField(max_length=250)
    email = models.CharField(max_length=250)
    message = models.TextField()
    field = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

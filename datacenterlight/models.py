from django.db import models


class VMTemplate(models.Model):
    name = models.CharField(max_length=50)
    opennebula_vm_template_id = models.IntegerField()

    @classmethod
    def create(cls, name, opennebula_vm_template_id):
        vm_template = cls(
            name=name, opennebula_vm_template_id=opennebula_vm_template_id)
        return vm_template


class VMPricing(models.Model):
    name = models.CharField(max_length=255, unique=True)
    vat_inclusive = models.BooleanField(default=True)
    vat_percentage = models.DecimalField(
        max_digits=7, decimal_places=2, blank=True, default=0
    )
    cores_unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0
    )
    ram_unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0
    )
    ssd_unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0
    )
    hdd_unit_price = models.DecimalField(
        max_digits=7, decimal_places=2, default=0
    )

    def __str__(self):
        return self.name + '-' + 'VAT' if self.vat_inclusive else 'NO_VAT'

    @classmethod
    def get_default_pricing(cls):
        """ Returns the default pricing or None """
        try:
            default_pricing = VMPricing.objects.get(name='default')
        except:
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

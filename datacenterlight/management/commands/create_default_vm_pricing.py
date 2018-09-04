from django.core.management.base import BaseCommand

from datacenterlight.models import VMPricing


class Command(BaseCommand):
    help = '''Creates default VMPricing object'''
    DEFAULT_VMPRICING_NAME = 'default'

    def handle(self, *args, **options):
        self.create_default_vm_pricing()

    def create_default_vm_pricing(self):
        obj, created = VMPricing.objects.get_or_create(
            name=self.DEFAULT_VMPRICING_NAME,
            defaults={
                "vat_inclusive": True,
                "cores_unit_price": 5,
                "ram_unit_price": 2,
                "ssd_unit_price": 0.6,
                "hdd_unit_price": 0.01
            }
        )

        if created:
            print(
                'Successfully created {} VMPricing object'.format(
                    self.DEFAULT_VMPRICING_NAME
                )
            )
        else:
            print(
                '{} VMPricing exists already.'.format(
                    self.DEFAULT_VMPRICING_NAME
                )
            )

from django.core.management.base import BaseCommand, CommandError
from hosting.models import VirtualMachineType


class Command(BaseCommand):
    help = 'Create VM types'

    def get_data(self):

        hetzner = {
            'base_price': 10,
            'core_price': 10,
            'memory_price': 5,
            'disk_size_price': 1,
            'description': 'VM auf einzelner HW, Raid1, kein HA'
        }

        return {
            'hetzner_nug': {
                'base_price': 5,
                'memory_price': 2,
                'core_price': 2,
                'disk_size_price': 0.5,
                'description': 'VM ohne Uptime Garantie'
            },
            'hetzner': hetzner,
            'hetzner_raid6': {
                'base_price': hetzner['base_price']*1.2,
                'core_price': hetzner['core_price']*1.2,
                'memory_price': hetzner['memory_price']*1.2,
                'disk_size_price': hetzner['disk_size_price']*1.2,
                'description': 'VM auf einzelner HW, Raid1, kein HA'

            },
            'hetzner_glusterfs': {
                'base_price': hetzner['base_price']*1.4,
                'core_price': hetzner['core_price']*1.4,
                'memory_price': hetzner['memory_price']*1.4,
                'disk_size_price': hetzner['disk_size_price']*1.4,
                'description': 'VM auf einzelner HW, Raid1, kein HA'
            },
            'bern': {
                'base_price': 12,
                'core_price': 25,
                'memory_price': 7,
                'disk_size_price': 0.70,
                'description': "VM in Bern, HA Setup ohne HA Garantie",
            }
        }

    def handle(self, *args, **options):

        data = self.get_data()
        [VirtualMachineType.objects.create(hosting_company=key, **data[key])
            for key in data.keys()]

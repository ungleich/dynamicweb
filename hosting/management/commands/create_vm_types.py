from django.core.management.base import BaseCommand, CommandError
from hosting.models import VirtualMachineType


class Command(BaseCommand):
    help = 'Create VM types'

    def get_data(self):

        return [
            {
                'base_price': 10,
                'core_price': 5,
                'memory_price': 2,
                'disk_size_price': 0.6,
                'cores': 1,
                'memory': 2,
                'disk_size': 10
            },
            {
                'base_price': 10,
                'core_price': 5,
                'memory_price': 2,
                'disk_size_price': 0.6,
                'cores': 1,
                'memory': 2,
                'disk_size': 100
            },
            {
                'base_price': 10,
                'core_price': 5,
                'memory_price': 2,
                'disk_size_price': 0.6,
                'cores': 2,
                'memory': 4,
                'disk_size': 20
            },
            {
                'base_price': 10,
                'core_price': 5,
                'memory_price': 2,
                'disk_size_price': 0.6,
                'cores': 4,
                'memory': 8,
                'disk_size': 40
            },
            {
                'base_price': 10,
                'core_price': 5,
                'memory_price': 2,
                'disk_size_price': 0.6,
                'cores': 16,
                'memory': 8,
                'disk_size': 40
            },
        ]


        hetzner = {
            'base_price': 10,
            'core_price': 5,
            'memory_price': 2,
            'disk_size_price': 0.6,
            'description': 'VM auf einzelner HW, Raid1, kein HA',
            'location': 'DE'
        }

        # return {
        #     # 'hetzner_nug': {
        #     #     'base_price': 5,
        #     #     'memory_price': 2,
        #     #     'core_price': 2,
        #     #     'disk_size_price': 0.5,
        #     #     'description': 'VM ohne Uptime Garantie'
        #     # },
        #     'hetzner': hetzner,
        #     # 'hetzner_raid6': {
        #     #     'base_price': hetzner['base_price']*1.2,
        #     #     'core_price': hetzner['core_price']*1.2,
        #     #     'memory_price': hetzner['memory_price']*1.2,
        #     #     'disk_size_price': hetzner['disk_size_price']*1.2,
        #     #     'description': 'VM auf einzelner HW, Raid1, kein HA'

        #     # },
        #     # 'hetzner_glusterfs': {
        #     #     'base_price': hetzner['base_price']*1.4,
        #     #     'core_price': hetzner['core_price']*1.4,
        #     #     'memory_price': hetzner['memory_price']*1.4,
        #     #     'disk_size_price': hetzner['disk_size_price']*1.4,
        #     #     'description': 'VM auf einzelner HW, Raid1, kein HA'
        #     # },
        #     'bern': {
        #         'base_price': 12,
        #         'core_price': 25,
        #         'memory_price': 7,
        #         'disk_size_price': 0.70,
        #         'description': "VM in Bern, HA Setup ohne HA Garantie",
        #         'location': 'CH',
        #     }
        # }

    def handle(self, *args, **options):

        vm_data = self.get_data()
        for vm in vm_data:
            VirtualMachineType.objects.create(**vm)

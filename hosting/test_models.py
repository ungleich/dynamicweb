# from django.test import TestCase
#
# from django.core.management import call_command
#
#
# #from .models import VirtualMachineType
#
#
# class VirtualMachineTypeModelTest(TestCase):
#
#     def setUp(self):
#         self.HETZNER_NUG_NAME = 'hetzner_nug'
#         self.HETZNER_NAME = 'hetzner'
#         self.HETZNER_RAID6_NAME = 'hetzner_raid6'
#         self.HETZNER_GLUSTERFS_NAME = 'hetzner_glusterfs'
#         self.BERN_NAME = 'bern'
#         self.HETZNER_NUG_EXPECTED_PRICE = 79
#         self.HETZNER_EXPECTED_PRICE = 180
#         self.HETZNER_RAID6_EXPECTED_PRICE = 216
#         self.HETZNER_GLUSTERFS_EXPECTED_PRICE = 252
#         self.BERN_EXPECTED_PRICE = 202
#
#         call_command('create_vm_types')
#
#     def test_calculate_price(self):
#
#         # hetzner_nug
#         # specifications = {
#         #     'cores': 2,
#         #     'memory': 10,
#         #     'disk_size': 100
#         # }
#         # vm_type = VirtualMachineType.objects.get(hosting_company=self.HETZNER_NUG_NAME)
#         # calculated_price = vm_type.calculate_price(specifications)
#         # self.assertEqual(calculated_price, self.HETZNER_NUG_EXPECTED_PRICE)
#
#         # hetzner
#         specifications = {
#             'cores': 2,
#             'memory': 10,
#             'disk_size': 100
#         }
#         vm_type = VirtualMachineType.objects.get(hosting_company=self.HETZNER_NAME)
#         calculated_price = vm_type.calculate_price(specifications)
#         self.assertEqual(calculated_price, self.HETZNER_EXPECTED_PRICE)
#
#         # hetzner_raid6
#         # specifications = {
#         #     'cores': 2,
#         #     'memory': 10,
#         #     'disk_size': 100
#         # }
#         # vm_type = VirtualMachineType.objects.get(hosting_company=self.HETZNER_RAID6_NAME)
#         # calculated_price = vm_type.calculate_price(specifications)
#         # self.assertEqual(calculated_price, self.HETZNER_RAID6_EXPECTED_PRICE)
#
#         # hetzner_glusterfs
#         # specifications = {
#         #     'cores': 2,
#         #     'memory': 10,
#         #     'disk_size': 100
#         # }
#         # vm_type = VirtualMachineType.objects.get(hosting_company=self.HETZNER_GLUSTERFS_NAME)
#         # calculated_price = vm_type.calculate_price(specifications)
#         # self.assertEqual(calculated_price, self.HETZNER_GLUSTERFS_EXPECTED_PRICE)
#
#         # bern
#         specifications = {
#             'cores': 2,
#             'memory': 10,
#             'disk_size': 100
#         }
#         vm_type = VirtualMachineType.objects.get(hosting_company=self.BERN_NAME)
#         calculated_price = vm_type.calculate_price(specifications)
#         self.assertEqual(calculated_price, self.BERN_EXPECTED_PRICE)

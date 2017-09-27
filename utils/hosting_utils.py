import logging
from oca.pool import WrongIdError

from hosting.models import UserHostingKey, VMDetail
from opennebula_api.serializers import VirtualMachineSerializer

logger = logging.getLogger(__name__)


def get_all_public_keys(customer):
    """
    Returns all the public keys of the user
    :param customer: The customer whose public keys are needed
    :return: A list of public keys
    """
    return UserHostingKey.objects.filter(user_id=customer.id).values_list(
        "public_key", flat=True)


def get_or_create_vm_detail(user, manager, vm_id):
    """
    Returns VMDetail object related to given vm_id. Creates the object
     if it does not exist

    :param vm_id: The ID of the VM which should be greater than 0.
    :param user: The CustomUser object that owns this VM
    :param manager: The OpenNebulaManager object
    :return: The VMDetail object. None if vm_id is less than or equal to 0.
    Also, for the cases where the VMDetail does not exist and we can not
    fetch data about the VM from OpenNebula, the function returns None
    """
    if vm_id <= 0:
        return None
    try:
        vm_detail_obj = VMDetail.objects.get(vm_id=vm_id)
    except VMDetail.DoesNotExist:
        try:
            vm_obj = manager.get_vm(vm_id)
        except (WrongIdError, ConnectionRefusedError) as e:
            logger.error(str(e))
            return None
        vm = VirtualMachineSerializer(vm_obj).data
        vm_detail_obj = VMDetail.objects.create(
            user=user, vm_id=vm_id, disk_size=vm['disk_size'],
            cores=vm['cores'], memory=vm['memory'],
            configuration=vm['configuration'], ipv4=vm['ipv4'],
            ipv6=vm['ipv6']
        )
    return vm_detail_obj


def get_vm_price(cpu, memory, disk_size):
    """
    A helper function that computes price of a VM from given cpu, ram and
    ssd parameters

    :param cpu: Number of cores of the VM
    :param memory: RAM of the VM
    :param disk_size: Disk space of the VM
    :return: The price of the VM
    """
    return (cpu * 5) + (memory * 2) + (disk_size * 0.6)

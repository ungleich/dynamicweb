import decimal
import logging
import subprocess
from oca.pool import WrongIdError

from datacenterlight.models import VMPricing
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


def get_vm_price(cpu, memory, disk_size, hdd_size=0, pricing_name='default'):
    """
    A helper function that computes price of a VM from given cpu, ram and
    ssd parameters

    :param cpu: Number of cores of the VM
    :param memory: RAM of the VM
    :param disk_size: Disk space of the VM (SSD)
    :param hdd_size: The HDD size
    :param pricing_name: The pricing name to be used
    :return: The price of the VM
    """
    try:
        pricing = VMPricing.objects.get(name=pricing_name)
    except Exception as ex:
        logger.error(
            "Error getting VMPricing object for {pricing_name}."
            "Details: {details}".format(
                pricing_name=pricing_name, details=str(ex)
            )
        )
        return None
    price = ((decimal.Decimal(cpu) * pricing.cores_unit_price) +
             (decimal.Decimal(memory) * pricing.ram_unit_price) +
             (decimal.Decimal(disk_size) * pricing.ssd_unit_price) +
             (decimal.Decimal(hdd_size) * pricing.hdd_unit_price))
    cents = decimal.Decimal('.01')
    price = price.quantize(cents, decimal.ROUND_HALF_UP)
    return float(price)


def get_vm_price_with_vat(cpu, memory, ssd_size, hdd_size=0,
                          pricing_name='default'):
    """
    A helper function that computes price of a VM from given cpu, ram and
    ssd, hdd and the pricing parameters

    :param cpu: Number of cores of the VM
    :param memory: RAM of the VM
    :param ssd_size: Disk space of the VM (SSD)
    :param hdd_size: The HDD size
    :param pricing_name: The pricing name to be used
    :return: The a tuple containing the price of the VM, the VAT and the
             VAT percentage
    """
    try:
        pricing = VMPricing.objects.get(name=pricing_name)
    except Exception as ex:
        logger.error(
            "Error getting VMPricing object for {pricing_name}."
            "Details: {details}".format(
                pricing_name=pricing_name, details=str(ex)
            )
        )
        return None

    price = (
        (decimal.Decimal(cpu) * pricing.cores_unit_price) +
        (decimal.Decimal(memory) * pricing.ram_unit_price) +
        (decimal.Decimal(ssd_size) * pricing.ssd_unit_price) +
        (decimal.Decimal(hdd_size) * pricing.hdd_unit_price)
    )
    if pricing.vat_inclusive:
        vat = decimal.Decimal(0)
        vat_percent = decimal.Decimal(0)
    else:
        vat = price * pricing.vat_percentage * decimal.Decimal(0.01)
        vat_percent = pricing.vat_percentage

    cents = decimal.Decimal('.01')
    price = price.quantize(cents, decimal.ROUND_HALF_UP)
    vat = vat.quantize(cents, decimal.ROUND_HALF_UP)
    discount = {
        'name': pricing.discount_name,
        'amount': float(pricing.discount_amount),
    }
    return float(price), float(vat), float(vat_percent), discount


def ping_ok(host_ipv6):
    """
    A utility method to check if a host responds to ping requests. Note: the
    function relies on `ping6` utility of debian to check.

    :param host_ipv6 str type parameter that represets the ipv6 of the host to
           checked
    :return True if the host responds to ping else returns False
    """
    try:
        subprocess.check_output("ping6 -c 1 " + host_ipv6, shell=True)
    except Exception as ex:
        logger.debug(host_ipv6 + " not reachable via ping. Error = " + str(ex))
        return False
    return True


class HostingUtils:
    @staticmethod
    def clear_items_from_list(from_list, items_list):
        """
        A utility function to clear items from a given list.
        Useful when deleting items in bulk from session.
        e.g.:
        HostingUtils.clear_items_from_list(
            request.session,
            ['token', 'billing_address_data', 'card_id',]
        )
        :param from_list:
        :param items_list:
        :return:
        """
        for var in items_list:
            if var in from_list:
                del from_list[var]

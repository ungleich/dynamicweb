from hosting.models import UserHostingKey


def get_all_public_keys(customer):
    """
    Returns all the public keys of the user
    :param customer: The customer whose public keys are needed
    :return: A list of public keys
    """
    return UserHostingKey.objects.filter(user_id=customer.id).values_list(
        "public_key", flat=True)


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

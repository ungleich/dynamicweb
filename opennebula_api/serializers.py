import ipaddress
from builtins import hasattr

from oca import OpenNebulaException
from rest_framework import serializers

from .models import OpenNebulaManager


class VirtualMachineTemplateSerializer(serializers.Serializer):
    """Serializer to map the virtual machine template instance into JSON format."""
    id = serializers.IntegerField(read_only=True)
    name = serializers.SerializerMethodField()
    cores = serializers.SerializerMethodField()
    disk_size = serializers.SerializerMethodField()
    memory = serializers.SerializerMethodField()

    def get_cores(self, obj):
        if hasattr(obj.template, 'vcpu'):
            return obj.template.vcpu

        return ''

    def get_disk_size(self, obj):
        template = obj.template
        disk_size = 0
        try:
            for disk in template.disks:
                disk_size += int(disk.size)
            return disk_size / 1024
        except:
            return 0

    def get_memory(self, obj):
        return int(obj.template.memory) / 1024

    def get_name(self, obj):
        return obj.name.strip('public-')


class VirtualMachineSerializer(serializers.Serializer):
    """Serializer to map the virtual machine instance into JSON format."""

    name = serializers.SerializerMethodField()
    cores = serializers.IntegerField(source='template.vcpu')
    disk = serializers.IntegerField(write_only=True)
    set_memory = serializers.IntegerField(write_only=True, label='Memory')
    memory = serializers.SerializerMethodField()

    disk_size = serializers.SerializerMethodField()
    hdd_size = serializers.SerializerMethodField()
    ssd_size = serializers.SerializerMethodField()
    ipv4 = serializers.SerializerMethodField()
    ipv6 = serializers.SerializerMethodField()
    vm_id = serializers.IntegerField(read_only=True, source='id')
    state = serializers.CharField(read_only=True, source='str_state')
    price = serializers.SerializerMethodField()
    ssh_key = serializers.CharField(write_only=True)
    configuration = serializers.SerializerMethodField()

    template_id = serializers.ChoiceField(
        choices=[(key.id, key.name) for key in
                 OpenNebulaManager().try_get_templates()
                 ],
        source='template.template_id',
        write_only=True,
        default=[]
    )

    def create(self, validated_data):
        owner = validated_data['owner']
        ssh_key = validated_data['ssh_key']
        cores = validated_data['template']['vcpu']
        memory = validated_data['set_memory']
        disk = validated_data['disk']

        template_id = validated_data['template']['template_id']
        specs = {
            'cpu': cores,
            'disk_size': disk,
            'memory': memory,
        }

        try:
            manager = OpenNebulaManager(email=owner.email,
                                        password=owner.password,
                                        )
            opennebula_id = manager.create_vm(template_id=template_id,
                                              ssh_key=ssh_key,
                                              specs=specs)
        except OpenNebulaException as err:
            raise serializers.ValidationError(
                "OpenNebulaException occured. {0}".format(err)
            )

        return manager.get_vm(opennebula_id)

    def get_memory(self, obj):
        return int(obj.template.memory) / 1024

    def get_disk_size(self, obj):
        template = obj.template
        disk_size = 0
        for disk in template.disks:
            disk_size += int(disk.size)
        return disk_size / 1024

    def get_ssd_size(self, obj):
        template = obj.template
        disk_size = 0
        for disk in template.disks:
            if disk.datastore == 'cephds':
                disk_size += int(disk.size)
        return disk_size / 1024

    def get_hdd_size(self, obj):
        template = obj.template
        disk_size = 0
        for disk in template.disks:
            if disk.datastore == 'ceph_hdd_ds':
                disk_size += int(disk.size)
        return disk_size / 1024

    def get_price(self, obj):
        template = obj.template
        return get_vm_price(
            cpu=int(template.vcpu), memory=self.get_disk_size(obj),
            ssd_size=self.get_ssd_size(obj), hdd_size=self.get_hdd_size(obj)
        )

    def get_configuration(self, obj):
        template_id = obj.template.template_id
        template = OpenNebulaManager().get_template(template_id)
        return template.name.strip('public-')

    def get_ipv4(self, obj):
        """
        Get the IPv4s from the given VM

        :param obj: The VM in contention
        :return: Returns csv string of all IPv4s added to this VM otherwise returns "-" if no IPv4 is available
        """
        ipv4 = []
        for nic in obj.template.nics:
            if hasattr(nic, 'ip'):
                ipv4.append(nic.ip)
        if len(ipv4) > 0:
            return ', '.join(ipv4)
        else:
            return '-'

    def get_ipv6(self, obj):
        ipv6 = []
        for nic in obj.template.nics:
            if hasattr(nic, 'ip6_global'):
                ipv6.append(nic.ip6_global)
        if len(ipv6) > 0:
            return ', '.join(ipv6)
        else:
            return '-'

    def get_name(self, obj):
        return obj.name.strip('public-')


class VMTemplateSerializer(serializers.Serializer):
    """Serializer to map the VMTemplate instance into JSON format."""
    id = serializers.IntegerField(
        read_only=True, source='opennebula_vm_template_id'
    )
    name = serializers.CharField(read_only=True)


def hexstr2int(string):
    return int(string.replace(':', ''), 16)


FIRST_MAC = hexstr2int('02:00:b3:39:79:4d')
FIRST_V4 = ipaddress.ip_address('185.203.112.2')
COUNT = 1000


def v4_from_mac(mac):
    """Calculates the IPv4 address from a MAC address.

    mac: string (the colon-separated representation)
    returns: ipaddress.ip_address object with the v4 address
    """
    return FIRST_V4 + (hexstr2int(mac) - FIRST_MAC)


def is_in_v4_range(mac):
    return FIRST_MAC <= hexstr2int(mac) < FIRST_MAC + 1000


def get_vm_price(cpu, memory, ssd_size, hdd_size=0):
    """
    A helper function that computes price of a VM from given cpu, ram and
    ssd_size, hdd_size parameters

    :param cpu: Number of cores of the VM
    :param memory: RAM of the VM
    :param ssd_size: SSD space of the VM
    :param hdd_size: Hard disk space of the VM
    :return: The price of the VM
    """
    return (cpu * 5) + (memory * 2) + (ssd_size * 0.6) + (hdd_size * 0.01)

import oca

from rest_framework import serializers

from oca import OpenNebulaException
from oca.template import VmTemplate

from .models import OpenNebulaManager

class VirtualMachineTemplateSerializer(serializers.Serializer):
    """Serializer to map the virtual machine template instance into JSON format."""
    id          = serializers.IntegerField(read_only=True)
    set_name    = serializers.CharField(read_only=True, label='Name')
    name        = serializers.SerializerMethodField()
    cores       = serializers.IntegerField(source='template.vcpu') 
    disk        = serializers.IntegerField(write_only=True)
    disk_size   = serializers.SerializerMethodField()
    set_memory      = serializers.IntegerField(write_only=True, label='Memory')
    memory      = serializers.SerializerMethodField()
    price       = serializers.SerializerMethodField()

    def create(self, validated_data):
        data = validated_data
        template = data.pop('template')

        cores = template.pop('vcpu')
        name    = data.pop('name')
        disk_size = data.pop('disk') 
        memory  = template.pop('memory')
        manager = OpenNebulaManager()
        
        try:
            opennebula_id = manager.create_template(name=name, cores=cores,
                                                    memory=memory,
                                                    disk_size=disk_size,
                                                    core_price=core_price,
                                                    disk_size_price=disk_size_price,
                                                    memory_price=memory_price)
        except OpenNebulaException as err:
            raise serializers.ValidationError("OpenNebulaException occured. {0}".format(err))
        
        return manager.get_template(template_id=opennebula_id)

    def get_disk_size(self, obj):
        template = obj.template
        disk_size = 0
        try:
            for disk in template.disks:
                disk_size += int(disk.size)
            return disk_size / 1024 
        except:
            return 0


    def get_price(self, obj):
        template = obj.template
        price = float(template.cpu) * 5.0
        price += (int(template.memory)/1024 * 2.0)
        try:
            for disk in template.disks:
                price += int(disk.size)/1024 * 0.6
        except:
            pass
        return price

    def get_memory(self, obj):
        return int(obj.template.memory)/1024

    def get_name(self, obj):
        # TODO: Filter public- away
        return obj.name

class VirtualMachineSerializer(serializers.Serializer):
    """Serializer to map the virtual machine instance into JSON format."""

    name        = serializers.CharField(read_only=True)
    cores       = serializers.IntegerField(source='template.vcpu') 
    disk        = serializers.IntegerField(write_only=True)
    set_memory      = serializers.IntegerField(write_only=True, label='Memory')
    memory      = serializers.SerializerMethodField()
    

    disk_size   = serializers.SerializerMethodField()
    ip          = serializers.CharField(read_only=True,
                                        source='user_template.ungleich_public_ip',
                                        default='-')
    vm_id       = serializers.IntegerField(read_only=True, source='id')
    state       = serializers.CharField(read_only=True, source='str_state')
    price       = serializers.SerializerMethodField()
    ssh_key     = serializers.CharField(write_only=True)

    template_id = serializers.ChoiceField(
                choices=[(key.id, key.name) for key in
                    OpenNebulaManager().get_templates()],
                source='template.template_id',
                write_only=True
            )

    def create(self, validated_data):
        owner = validated_data['owner']
        ssh_key = validated_data['ssh_key']
        cores = validated_data['template']['vcpu']
        memory = validated_data['set_memory']
        disk = validated_data['disk']

        template_id = validated_data['template']['template_id']
        specs = {
                    'cpu' : cores,
                    'disk_size' : disk,
                    'memory' : memory,
                }


        try:
            manager = OpenNebulaManager(email=owner.email,
                                        password=owner.password,
                                        )
            opennebula_id = manager.create_vm(template_id=template_id,
                                              ssh_key=ssh_key,
                                              specs=specs)
        except OpenNebulaException as err:
            raise serializers.ValidationError("OpenNebulaException occured. {0}".format(err))
        
        return manager.get_vm(opennebula_id)

    def get_memory(self, obj):
        return int(obj.template.memory)/1024

    def get_disk_size(self, obj):
        template = obj.template
        disk_size = 0
        for disk in template.disks:
            disk_size += int(disk.size)
        return disk_size / 1024

    def get_price(self, obj):
        template = obj.template
        price = float(template.cpu) * 5.0
        price += (int(template.memory)/1024 * 2.0)
        for disk in template.disks:
            price += int(disk.size)/1024 * 0.6
        return price

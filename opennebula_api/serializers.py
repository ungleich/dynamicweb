import oca

from rest_framework import serializers

from oca import OpenNebulaException

from .models import VirtualMachine, VirtualMachineTemplate, OpenNebulaManager

class VirtualMachineTemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the virtual machine template instance into JSON format."""
    cores       = serializers.IntegerField(source='get_cores') 
    name        = serializers.CharField(source='get_name')
    disk_size   = serializers.IntegerField(source='get_disk_size')
    memory      = serializers.IntegerField(source='get_memory')

    class Meta:
        model = VirtualMachineTemplate
        fields = ('id', 'name', 'cores', 'memory', 'disk_size', 'base_price', 
                  'core_price', 'memory_price', 'disk_size_price', 'opennebula_id')
        read_only_fields = ('opennebula_id', )

    def validate(self, data):
        # Create the opennebula model
        cores   = data.pop('get_cores')
        name    = data.pop('get_name')
        disk_size = data.pop('get_disk_size')
        memory  = data.pop('get_memory')

        manager = OpenNebulaManager(create_user = False)
        
        try:
            opennebula_id = manager.create_template(name=name, cores=cores,
                                                    memory=memory,
                                                    disk_size=disk_size)
            data.update({'opennebula_id':opennebula_id})
        except OpenNebulaException as err:
            raise serializers.ValidationError("OpenNebulaException occured. {0}".format(err))
        
        return data

    def create(self, validated_data):
        return VirtualMachineTemplate.objects.create(**validated_data)

class TemplatePrimaryKeyRelatedField(serializers.PrimaryKeyRelatedField):
    def display_value(self, instance):
        return 'Template: {}'.format(instance.get_name())

class VirtualMachineSerializer(serializers.ModelSerializer):
    """Serializer to map the virtual machine instance into JSON format."""

    #TODO: Maybe we can change to template.get_cores
    cores       = serializers.IntegerField(read_only=True, source='get_cores') 
    name        = serializers.CharField(read_only=True, source='get_name')
    disk_size   = serializers.IntegerField(read_only=True, source='get_disk_size')
    memory      = serializers.IntegerField(read_only=True, source='get_memory')
    #TODO: See if we can change to IPAddressField
    ip          = serializers.CharField(read_only=True, source='get_ip')
    deploy_id   = serializers.IntegerField(read_only=True, source='get_deploy_id')
    vm_id          = serializers.IntegerField(read_only=True, source='get_vm_id')
    state       = serializers.CharField(read_only=True, source='get_state')
    price       = serializers.FloatField(read_only=True, source='get_price')

    owner = serializers.ReadOnlyField(source='owner.name')

    vm_template = VirtualMachineTemplateSerializer(read_only=True)

    vm_template_id = TemplatePrimaryKeyRelatedField(
                queryset=VirtualMachineTemplate.objects.all(),
                source='vm_template'
            )

    class Meta:
        model = VirtualMachine
        fields = ('id', 'opennebula_id', 'vm_template', 'vm_template_id', 'cores', 'name',
                'disk_size', 'memory', 'ip', 'deploy_id', 'state', 'vm_id',
                'price', 'owner')
        read_only_fields = ('opennebula_id', )

    def validate(self, data):
        # Create the opennebula model
        
        try:
            template_id = data['vm_template'].opennebula_id
            owner = self.context.get('request').user
            manager = OpenNebulaManager(email=owner.email,
                                        password=owner.password[0:20],
                                        create_user = True)
            opennebula_id = manager.create_vm(template_id)
            data.update({'opennebula_id':opennebula_id})
        except OpenNebulaException as err:
            raise serializers.ValidationError("OpenNebulaException occured. {0}".format(err))
        
        return data

    def create(self, validated_data):
        return VirtualMachine.objects.create(**validated_data)

    def update(self, instance, validated_data):
        pass

    def delete(self, instance, validated_data):
        try:
            owner = instance.owner
            manager = OpenNebulaManager(email=owner.email,
                                        password=owner.password[0:20],
                                        create_user = True)
            manager.delete_vm(template_id)
        except OpenNebulaException as err:
            raise serializers.ValidationError("OpenNebulaException occured. {0}".format(err))



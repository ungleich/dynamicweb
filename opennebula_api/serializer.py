from res_framework import serializers
from .models import VirtualMachine, VirtualMachineTemplate

class VirtualMachineSerializer(serializers.ModelSerializer):
    """Serializer to map the virtual machine instance into JSON format."""

    cores       = serializers.IntegerField(read_only=True, source='get_cores') 
    name        = serializers.CharField(read_only=True, source='get_name')
    disk_size   = serializers.IntegerField(read_only=True, source='get_disk_size')
    memory      = serializers.IntegerField(read_only=True, source='get_memory')
    #TODO: See if we can change to IPAddressField
    ip          = serializers.CharField(read_only=True, source='get_ip')
    deploy_id   = serializers.IntegerField(read_only=True, source='get_deploy_id')
    id          = serializers.IntegerField(read_only=True, source='get_id')
    state       = serializers.CharField(read_only=True, source='get_state')
    price       = serializers.FloatField(read_only=True, source='get_price')

    class Meta:
        model = VirtualMachine


class VirtualMachineTemplateSerializer(serializers.ModelSerializer):
    """Serializer to map the virtual machine template instance into JSON format."""
    cores       = serializers.IntegerField(read_only=True, source='get_cores') 
    name        = serializers.CharField(read_only=True, source='get_name')
    disk_size   = serializers.IntegerField(read_only=True, source='get_disk_size')
    memory      = serializers.IntegerField(read_only=True, source='get_memory')

    class Meta:
        model = VirtualMachineTemplate
        fields = ()


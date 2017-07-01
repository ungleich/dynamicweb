from rest_framework import generics
from rest_framework import permissions

from .serializers import VirtualMachineSerializer
from .models import OpenNebulaManager
from rest_framework.exceptions import APIException


class ServiceUnavailable(APIException):
    status_code = 503
    default_detail = 'Service temporarily unavailable, try again later.'
    default_code = 'service_unavailable'


class VmCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests."""
    serializer_class = VirtualMachineSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # We may have ConnectionRefusedError if we don't have a
        # connection to OpenNebula. For now, we raise ServiceUnavailable
        try:
            vms = manager.get_vms()
        except ConnectionRefusedError:
            raise ServiceUnavailable
        return vms

    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save(owner=self.request.user)


class VmDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    permission_classes = (permissions.IsAuthenticated, )

    serializer_class = VirtualMachineSerializer

    def get_queryset(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # We may have ConnectionRefusedError if we don't have a
        # connection to OpenNebula. For now, we raise ServiceUnavailable
        try:
            vms = manager.get_vms()
        except ConnectionRefusedError:
            raise ServiceUnavailable
        return vms

    def get_object(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # We may have ConnectionRefusedError if we don't have a
        # connection to OpenNebula. For now, we raise ServiceUnavailable
        try:
            vm = manager.get_vm(self.kwargs.get('pk'))
        except ConnectionRefusedError:
            raise ServiceUnavailable
        return vm

    def perform_destroy(self, instance):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password)
        # We may have ConnectionRefusedError if we don't have a
        # connection to OpenNebula. For now, we raise ServiceUnavailable
        try:
            manager.delete_vm(instance.id)
        except ConnectionRefusedError:
            raise ServiceUnavailable

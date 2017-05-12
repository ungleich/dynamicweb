from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login


from utils.views import LoginViewMixin
from membership.models import CustomUser, StripeCustomer
from guardian.mixins import PermissionRequiredMixin

from .serializers import VirtualMachineTemplateSerializer, \
                         VirtualMachineSerializer
from .models import OpenNebulaManager


class TemplateCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests."""

    serializer_class = VirtualMachineTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def get_queryset(self):
        manager = OpenNebulaManager()
        return manager.get_templates()


    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save()

class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    serializer_class = VirtualMachineTemplateSerializer
    permission_classes = (permissions.IsAuthenticated)

    def get_queryset(self):
        manager = OpenNebulaManager()
        return manager.get_templates()

class VmCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests."""
    serializer_class = VirtualMachineSerializer
    permission_classes = (permissions.IsAuthenticated, )

    def get_queryset(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password,
                                    create_user=True)
        return manager.get_vms()

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
                                    password=owner.password,
                                    create_user=True)
        return manager.get_vms()

    def get_object(self):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password,
                                    create_user=True)
        return manager.get_vm(self.kwargs.get('pk'))

    def perform_destroy(self, instance):
        owner = self.request.user
        manager = OpenNebulaManager(email=owner.email,
                                    password=owner.password,
                                    create_user = True)
        manager.delete_vm(instance.id)


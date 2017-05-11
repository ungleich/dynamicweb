from rest_framework import generics
from rest_framework import permissions

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth import authenticate, login


from utils.views import LoginViewMixin
from membership.models import CustomUser, StripeCustomer
from guardian.mixins import PermissionRequiredMixin

from .serializers import VirtualMachineTemplateSerializer, \
                         VirtualMachineSerializer
from .models import VirtualMachineTemplate, VirtualMachine, OpenNebulaManager
from .permissions import IsOwner


class TemplateCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests."""

    queryset = VirtualMachineTemplate.objects.all()
    serializer_class = VirtualMachineTemplateSerializer
    permission_classes = (permissions.IsAuthenticated, permissions.IsAdminUser)

    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save()

class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = VirtualMachineTemplate.objects.all()
    serializer_class = VirtualMachineTemplateSerializer
    permission_classes = (permissions.IsAuthenticated)

class VmCreateView(generics.ListCreateAPIView):
    """This class handles the GET and POST requests."""
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save(owner=self.request.user)

class VmDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""
    permission_classes = (permissions.IsAuthenticated, IsOwner)

    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

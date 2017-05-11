from rest_framework import generics

from .serializers import VirtualMachineTemplateSerializer, \
                         VirtualMachineSerializer
from .models import VirtualMachineTemplate, VirtualMachine, OpenNebulaManager

class TemplateCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = VirtualMachineTemplate.objects.all()
    serializer_class = VirtualMachineTemplateSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save()

class TemplateDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = VirtualMachineTemplate.objects.all()
    serializer_class = VirtualMachineTemplateSerializer

class VmCreateView(generics.ListCreateAPIView):
    """This class defines the create behavior of our rest api."""
    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

    def perform_create(self, serializer):
        """Save the post data when creating a new template."""
        serializer.save()

class VmDetailsView(generics.RetrieveUpdateDestroyAPIView):
    """This class handles the http GET, PUT and DELETE requests."""

    queryset = VirtualMachine.objects.all()
    serializer_class = VirtualMachineSerializer

from django.contrib import admin
from .models import RailsBetaUser, VirtualMachineType

admin.site.register(RailsBetaUser, VirtualMachineType)

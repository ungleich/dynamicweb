from django.contrib import admin
from .models import RailsBetaUser, VirtualMachineType, HostingOrder, VirtualMachinePlan

admin.site.register(RailsBetaUser)
admin.site.register(VirtualMachineType)
admin.site.register(HostingOrder)
admin.site.register(VirtualMachinePlan)


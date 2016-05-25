from django.contrib import admin
from .models import VirtualMachineType, VirtualMachinePlan


admin.site.register(VirtualMachineType)
admin.site.register(VirtualMachinePlan)

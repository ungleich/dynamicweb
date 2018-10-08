from django.contrib import admin

from .models import HostingOrder, HostingBill, HostingPlan, GenericProduct

admin.site.register(HostingOrder)
admin.site.register(HostingBill)
admin.site.register(HostingPlan)
admin.site.register(GenericProduct)

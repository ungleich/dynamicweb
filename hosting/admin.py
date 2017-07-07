from django.contrib import admin

from .models import HostingOrder, HostingBill, HostingPlan


admin.site.register(HostingOrder)
admin.site.register(HostingBill)
admin.site.register(HostingPlan)

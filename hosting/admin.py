from django.contrib import admin

from utils.mailer import BaseEmail
from .models import VirtualMachineType, VirtualMachinePlan


class VirtualMachinePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email')

    def email(self, obj):
        return obj.hosting_orders.latest('id').customer.user.email

    def save_model(self, request, obj, form, change):
        email = self.email(obj)
        if 'status' in form.changed_data and obj.status == VirtualMachinePlan.ONLINE_STATUS:
            context = {
                'vm': obj
            }
            email_data = {
                'subject': 'Your VM has been activated',
                'to': email,
                'context': context,
                'template_name': 'vm_activated',
                'template_path': 'emails/'
            }
            email = BaseEmail(**email_data)
            email.send()
        obj.save()


admin.site.register(VirtualMachineType)
admin.site.register(VirtualMachinePlan, VirtualMachinePlanAdmin)

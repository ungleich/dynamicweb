from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse

from utils.mailer import BaseEmail

from .forms import HostingOrderAdminForm
from .models import VirtualMachineType, VirtualMachinePlan, HostingOrder, ManageVM
from .opennebula_functions import HostingManageVMAdmin


class HostingOrderAdmin(admin.ModelAdmin):
    # fields = ('slug', 'imdb_link', 'start', 'finish', 'added_by')
    list_display = ('id', 'created_at', 'plan', 'user')
    search_fields = ['vm_plan__id', 'customer__user__email']

    def save_model(self, request, obj, form, change):
        if not change:
            customer = form.cleaned_data.get('customer')

            # Get and set billing address from the lastest charged order
            last_order = HostingOrder.objects.filter(customer=customer).latest('id')
            billing_address = last_order.billing_address
            obj.billing_address = billing_address

            charge = form.cleaned_data.get('charge')
            # Associate an order with a stripe payment
            obj.set_stripe_charge(charge)

            # If the Stripe payment was successed, set order status approved
            obj.set_approved()

            # Assigning permissions
            obj.assign_permissions(customer.user)

            context = {
                'order': obj,
                'vm': obj.vm_plan,
                'base_url': "{0}://{1}".format(request.scheme, request.get_host())
            }
            email_data = {
                'subject': 'Your VM plan has been charged',
                'to': obj.customer.user.email,
                'context': context,
                'template_name': 'vm_charged',
                'template_path': 'hosting/emails/'
            }
            email = BaseEmail(**email_data)
            email.send()

        obj.save()
        return obj

    def get_form(self, request, obj=None, **kwargs):
        if obj is None:
            kwargs['form'] = HostingOrderAdminForm
        return super(HostingOrderAdmin, self).get_form(request, obj, **kwargs)

    def user(self, obj):
        email = obj.customer.user.email
        user_url = reverse("admin:membership_customuser_change", args=[obj.customer.user.id])
        return format_html("<a href='{url}'>{email}</a>", url=user_url, email=email)

    def plan(self, obj):
        vm_name = obj.vm_plan.name
        vm_url = reverse("admin:hosting_virtualmachineplan_change", args=[obj.vm_plan.id])
        return format_html("<a href='{url}'>{vm_name}</a>", url=vm_url, vm_name=vm_name)

    plan.short_description = "Virtual Machine Plan"


class VirtualMachinePlanAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'email')

    def email(self, obj):
        return obj.hosting_orders.latest('id').customer.user.email

    def save_model(self, request, obj, form, change):
        email = self.email(obj)
        if 'status' in form.changed_data:
            context = {
                'vm': obj,
                'base_url': "{0}://{1}".format(request.scheme, request.get_host())
            }
            email_data = {
                'subject': 'Your VM has been activated',
                'to': email,
                'context': context,
                'template_name': 'vm_status_changed',
                'template_path': 'hosting/emails/'
            }
            email = BaseEmail(**email_data)
            email.send()
        obj.save()


admin.site.register(HostingOrder, HostingOrderAdmin)
admin.site.register(VirtualMachineType)
admin.site.register(VirtualMachinePlan, VirtualMachinePlanAdmin)
admin.site.register(ManageVM, HostingManageVMAdmin)

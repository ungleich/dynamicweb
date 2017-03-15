from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.conf import settings
from utils.mailer import BaseEmail
from django import template
import oca
import socket
from oca.exceptions import OpenNebulaException

from .forms import HostingOrderAdminForm
from .models import VirtualMachineType, VirtualMachinePlan, HostingOrder, ManageVMs

register = template.Library()

def get_vm_state(value):
    if value == 1:
         return 'PENDING'
    #states = {-2: 'Any incl done', -1 : 'Any except done', 0 : 'INIT', 1 : 'PENDING', 2 : 'HOLD', 3 : 'ACTIVE', 4 : 'STOPPED', 5 : 'SUSPENDED', 6 : 'DONE', 7 : 'FAILED'}
    #return states.get(value)
    return 'UNKNO'

register.filter('get_vm_state', get_vm_state)

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

class HostingManageVMsAdmin(admin.ModelAdmin):
    client = None
    def get_urls(self):
        urls = super().get_urls()
        socket.setdefaulttimeout(5)
        my_urls = [
            url(r'^$', self.admin_site.admin_view(self.my_view, cacheable=True)),
            url(r'^create_vm/$', self.admin_site.admin_view(self.create_vm, cacheable=True), name='createvm'),
            #url(r'^my_views/$', self.admin_site.admin_view(self.my_view, cacheable=True))
        ]
        return my_urls + urls

    def my_view(self, request):
        s_message = ''
        e_message = ''
        try :
            client = oca.Client(settings.OPENNEBULA_USERNAME + ':' + settings.OPENNEBULA_PASSWORD, settings.OPENNEBULA_PROTOCOL + '://' + settings.OPENNEBULA_DOMAIN + ':' + settings.OPENNEBULA_PORT + settings.OPENNEBULA_ENDPOINT)
            vm_pool = oca.VirtualMachinePool(client)
            vm_pool.info()
            for vm in vm_pool:
               vm.info()
               print("%s (memory: %s MB)" % ( vm.name, vm.template.memory))
               
        except socket.timeout:
            e_message = "Socket timeout error."
        except OpenNebulaException:
            e_message = "OpenNebulaException occurred."           
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            error_msg = e_message,
            success_msg = s_message,           
            vms = vm_pool,
            # Anything else you want in the context...
            # key=value,
        )
        return TemplateResponse(request, "hosting/managevms.html", context)

    def create_vm(self, request):
        s_message = ''
        e_message = ''
        try :
            client = oca.Client(settings.OPENNEBULA_USERNAME + ':' + settings.OPENNEBULA_PASSWORD, settings.OPENNEBULA_PROTOCOL + '://' + settings.OPENNEBULA_DOMAIN + ':' + settings.OPENNEBULA_PORT + settings.OPENNEBULA_ENDPOINT)
            # Lets create a test VM with 128MB of ram and 1 CPU
            vm_id = oca.VirtualMachine.allocate(client, '<VM><MEMORY>128</MEMORY><CPU>1</CPU></VM>')
            s_message = "Created with id = " + str(vm_id)
            # Lets print the VMs available in the pool
            # print("Printing the available VMs in the pool.")
            # vm_pool = oca.VirtualMachinePool(client)
            # for vm in vm_pool:
            # 	print("%s (memory: %s MB)" % ( vm.name, vm.template.memory))
        except socket.timeout:
            e_message = "Socket timeout error."
        except OpenNebulaException:
            e_message = "OpenNebulaException occurred."
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            error_msg=e_message,
            success_msg=s_message,
            # Anything else you want in the context...
            # key=value,
        )
        return TemplateResponse(request, "hosting/managevms.html", context)
    
    def get_vms():
        vm_pool = oca.VirtualMachinePool(self.client)
        return vm_pool

admin.site.register(HostingOrder, HostingOrderAdmin)
admin.site.register(VirtualMachineType)
admin.site.register(VirtualMachinePlan, VirtualMachinePlanAdmin)
admin.site.register(ManageVMs, HostingManageVMsAdmin)

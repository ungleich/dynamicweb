from django.contrib import admin
from django.utils.html import format_html
from django.core.urlresolvers import reverse
from django.conf.urls import url
from django.template.response import TemplateResponse
from django.conf import settings
from utils.mailer import BaseEmail
from django import template
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.signals import user_logged_in
import random
import string

import oca
import socket
from oca.exceptions import OpenNebulaException

from .forms import HostingOrderAdminForm
from .models import VirtualMachineType, VirtualMachinePlan, HostingOrder, ManageVM

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

class HostingManageVMAdmin(admin.ModelAdmin):
    client = None
    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(self.my_view, cacheable=True), name='showvms'),
            url(r'^create_vm/$', self.admin_site.admin_view(self.create_vm, cacheable=True), name='createvm'),
            url(r'^delete_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.delete_vm, cacheable=True), name='deletevm'),
            url(r'^stop_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.stop_vm, cacheable=True), name='stopvm'),
            url(r'^start_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.start_vm, cacheable=True), name='startvm'),
        ]
        return my_urls + urls
    
    # Function to initialize opennebula client based on the logged in 
    # user
    def init_opennebula_client(self, opennebula_user):
        opennebula_user_password = get_random_password()
        self.client = oca.Client(opennebula_user + ':' + opennebula_user_password, settings.OPENNEBULA_PROTOCOL + '://' + settings.OPENNEBULA_DOMAIN + ':' + settings.OPENNEBULA_PORT + settings.OPENNEBULA_ENDPOINT)

    # Function that lists the VMs of the current user
    def my_view(self, request):
        try :
            self.init_opennebula_client(str(request.user))
            vm_pool = oca.VirtualMachinePool(self.client)
            vm_pool.info()
        except socket.timeout:
            messages.add_message(request, messages.ERROR, "Socket timeout error.")
        except OpenNebulaException:
            messages.add_message(request, messages.ERROR, "OpenNebulaException occurred.")
        except OSError as err:
            messages.add_message(request, messages.ERROR, str("OS error: {0}".format(err)))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            vms = vm_pool,
        )

        return TemplateResponse(request, "hosting/managevms.html", context)
  
    # Creating VM by using method allocate(client, template)
    def create_vm(self, request):
        message = ''
        # check if the request contains the template parameter, if it is 
        # not set warn the user of setting this.
        vm_template = request.POST.get('vm_template')
        if vm_template == 'select' :
            messages.add_message(request, messages.ERROR, "Please select a vm template")
        else :
            try :
                # We do have the vm_template param set. Get and parse it
                # and check it to be in the desired range.
                vm_template_int = int(vm_template)
                if vm_template_int >=1 and vm_template_int <= 8:
                    # Lets create a test VM with 128MB of ram and 1 CPU
                    vm_id = oca.VirtualMachine.allocate(self.client, '<VM><MEMORY>' + str(1024 * vm_template_int) + '</MEMORY><VCPU>' + str(vm_template_int)+ '</VCPU><CPU>' + str(0.1 * vm_template_int) + '</CPU><DISK><TYPE>fs</TYPE><SIZE>' + str(10000 * vm_template_int) + '</SIZE></DISK></VM>')
                    message = "Created with id = " + str(vm_id)
                    vm_pool = self.get_vms()
                    messages.add_message(request, messages.SUCCESS, message)                    
                else:
                    messages.add_message(request, messages.ERROR, "Please select an appropriate value for vm template.")
            except socket.timeout:
                messages.add_message(request, messages.ERROR, "Socket timeout error.")
            except OpenNebulaException:
                messages.add_message(request, messages.ERROR, "OpenNebulaException occurred.")
            except OSError as err:
                messages.add_message(request, messages.ERROR, str("OS error: {0}".format(err)))      
            except ValueError:
                messages.add_message(request, messages.ERROR, "Please select an appropriate value for vm template.")
        return redirect('admin:showvms')
   
    # Retrives virtual machine pool information
    def get_vms(self):
        vm_pool = oca.VirtualMachinePool(self.client)
        vm_pool.info()
        return vm_pool
        
    # Delete VM from the pool and DB by using method finalize()
    def delete_vm(self, request, vmid):
        # get the desired vm from the pool
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm == -1:
            messages.add_message(request, messages.ERROR, "Did not find a vm with id = " + str(vm_id))
        else :
            print("Deleting vm_id = " + str(vm_id) + " state = " + vm.str_state)
            if vm.str_state == 'PENDING' or vm.str_state =='POWEROFF' or vm.str_state =='ACTIVE':
                vm.delete()
                messages.add_message(request, messages.SUCCESS, "Deleted from " + vm.str_state + " state vm with id = " + str(vm_id))
            else:
                vm.finalize()
                messages.add_message(request, messages.SUCCESS, "Deleted (using finalize()) from " + vm.str_state + " state vm with id = " + str(vm_id))
        return redirect('admin:showvms')

    def stop_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm == -1:
            messages.add_message(request, messages.ERROR, "Did not find a vm with id = " + str(vm_id))
        else :
            vm.stop()
            messages.add_message(request, messages.SUCCESS, "Stopped the vm with id = " + str(vm_id))
        return redirect('admin:showvms')

    def start_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm == -1:
            messages.add_message(request, messages.ERROR, "Did not find a vm with id = " + str(vm_id))
        else :
            vm.resume()
            messages.add_message(request, messages.SUCCESS, "Started the vm with id = " + str(vm_id))
        return redirect('admin:showvms')

    def get_vm_by_id(self, vmid):
        vms = self.get_vms()
        vms
        for vm in vms:
            if vm.id == vmid :
                return vm
        return -1
        
# callback for creating opennebula users on user login
def user_logged_in_callback(sender, request, user, **kwargs):
    client = oca.Client(settings.OPENNEBULA_USERNAME + ':' + settings.OPENNEBULA_PASSWORD, settings.OPENNEBULA_PROTOCOL + '://' + settings.OPENNEBULA_DOMAIN + ':' + settings.OPENNEBULA_PORT + settings.OPENNEBULA_ENDPOINT)
    # Notes: 
    #     1. python-oca library's oca.User.allocate(client, user, pass)
    #     method does not work with python-oca version oca-4.15.0a1-py3.5
    #     This is because the call is missing a fourth parameter 
    #     auth_driver.
    #     To overcome this issue, we make a direct call to xml-rpc method
    #     'user.allocate' passing this fourth parameter.
    #
    #     2. We have a dummy authentication driver in opennebula and we
    #     use this so as to avoid opennebula authentication. However, we
    #     need to supply a dummy password. Without this, we can not 
    #     create an OpenNebula user. We use dummy string 'a' as password
    #     for all users.
    #
    #     3. We user the user's email as the user name.
    if find_opennebula_user_by_name(str(user.email), client) == -1 :
        user_id = client.call('user.allocate', str(user.email), get_random_password(), 'dummy')
        print("User " + str(user.email) + " does not exist. Created the user. User id = " + str(user_id))

# Finds if an OpenNebula user with user_name exists. Returns the 
# OpenNebula user if it exists, -1 otherwise.
def find_opennebula_user_by_name(user_name, client):
    pool = oca.UserPool(client)
    pool.info()
    for user in pool:
        if user.name == user_name :
            return user
    return -1
    
# Returns random password that is needed by OpenNebula
def get_random_password():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

user_logged_in.connect(user_logged_in_callback)

admin.site.register(HostingOrder, HostingOrderAdmin)
admin.site.register(VirtualMachineType)
admin.site.register(VirtualMachinePlan, VirtualMachinePlanAdmin)
admin.site.register(ManageVM, HostingManageVMAdmin)

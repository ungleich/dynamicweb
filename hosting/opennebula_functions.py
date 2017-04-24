import logging
import socket
import string

import oca
import random
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from oca.exceptions import OpenNebulaException

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HostingManageVMAdmin(admin.ModelAdmin):
    client = None

    def get_urls(self):
        urls = super().get_urls()
        my_urls = [
            url(r'^$', self.admin_site.admin_view(self.show_vms, cacheable=True), name='showvms'),
            url(r'^create_vm/$', self.admin_site.admin_view(self.create_vm, cacheable=True), name='createvm'),
            url(r'^delete_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.delete_vm, cacheable=True),
                name='deletevm'),
            url(r'^stop_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.stop_vm, cacheable=True), name='stopvm'),
            url(r'^start_vm/(?P<vmid>\d+)/$', self.admin_site.admin_view(self.start_vm, cacheable=True),
                name='startvm'),
        ]
        return my_urls + urls

    # Function to initialize opennebula client based on the logged in
    # user
    def init_opennebula_client(self, opennebula_user):
        if self.client is None:
            opennebula_user_password = get_random_password()
            self.client = oca.Client("{0}:{1}".format(opennebula_user, opennebula_user_password),
                                     "{protocol}://{domain}:{port}{endpoint}".format(
                                         protocol=settings.OPENNEBULA_PROTOCOL,
                                         domain=settings.OPENNEBULA_DOMAIN,
                                         port=settings.OPENNEBULA_PORT,
                                         endpoint=settings.OPENNEBULA_ENDPOINT
                                     ))

    # Function that shows the VMs of the current user
    def show_vms(self, request):
        vm_pool = None
        try:
            self.init_opennebula_client(request.user)
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
            vms=vm_pool,
        )

        return TemplateResponse(request, "hosting/managevms.html", context)

    # Creating VM by using method allocate(client, template)
    def create_vm(self, request):
        message = ''
        # check if the request contains the template parameter, if it is
        # not set warn the user of setting this.
        vm_template = request.POST.get('vm_template')
        if vm_template == 'select':
            messages.add_message(request, messages.ERROR, "Please select a vm template")
        else:
            try:
                # We do have the vm_template param set. Get and parse it
                # and check it to be in the desired range.
                # We have 8 possible VM templates for the moment which are 1x, 2x, 4x ...
                # the basic template of 10GB disk, 1GB ram, 1 vcpu, 0.1 cpu
                vm_template_int = int(vm_template)
                if 1 <= vm_template_int <= 8:
                    vm_string_formatter = """
                                            <VM>
                                              <MEMORY>
                                               {memory}
                                              </MEMORY>
                                              <VCPU>
                                               {vcpu}
                                              </VCPU>
                                              <CPU>
                                                {cpu}
                                              </CPU>
                                              <DISK>
                                                <TYPE>
                                                  {disk_type}
                                                </TYPE>
                                                <SIZE>
                                                  {size}
                                                </SIZE>
                                              </DISK>
                                            </VM>
                                            """
                    vm_id = oca.VirtualMachine.allocate(self.client,
                                                        vm_string_formatter.format(
                                                            memory=1024 * vm_template_int,
                                                            vcpu=vm_template_int,
                                                            cpu=0.1 * vm_template_int,
                                                            disk_type='fs',
                                                            size=10000 * vm_template_int))
                    message = "Created with id = " + str(vm_id)
                    messages.add_message(request, messages.SUCCESS, message)
                else:
                    messages.add_message(request, messages.ERROR,
                                         "Please select an appropriate value for vm template.")
            except socket.timeout as socket_err:
                messages.add_message(request, messages.ERROR, "Socket timeout error.")
                logger.error("Socket timeout error: {0}".format(socket_err))
            except OpenNebulaException as opennebula_err:
                messages.add_message(request, messages.ERROR, "OpenNebulaException occurred.")
                logger.error("OpenNebulaException error: {0}".format(opennebula_err))
            except OSError as os_err:
                messages.add_message(request, messages.ERROR, str("OS error: {0}".format(os_err)))
                logger.error("OSError : {0}".format(os_err))
            except ValueError as value_err:
                messages.add_message(request, messages.ERROR,
                                     "Please select an appropriate value for vm template.")
                logger.error("ValueError : {0}".format(value_err))
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
        else:
            print("Deleting vm_id = " + str(vm_id) + " state = " + vm.str_state)
            if vm.str_state == 'PENDING' or vm.str_state == 'POWEROFF' or vm.str_state == 'ACTIVE':
                vm.delete()
                messages.add_message(request, messages.SUCCESS,
                                     "Deleted from " + vm.str_state + " state vm with id = " + str(vm_id))
            else:
                vm.finalize()
                messages.add_message(request, messages.SUCCESS,
                                     "Deleted (using finalize()) from " + vm.str_state + " state vm with id = " + str(
                                         vm_id))
        return redirect('admin:showvms')

    def stop_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm == -1:
            messages.add_message(request, messages.ERROR, "Did not find a vm with id = " + str(vm_id))
        else:
            vm.stop()
            messages.add_message(request, messages.SUCCESS, "Stopped the vm with id = " + str(vm_id))
        return redirect('admin:showvms')

    def start_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm == -1:
            messages.add_message(request, messages.ERROR, "Did not find a vm with id = " + str(vm_id))
        else:
            vm.resume()
            messages.add_message(request, messages.SUCCESS, "Started the vm with id = " + str(vm_id))
        return redirect('admin:showvms')

    def get_vm_by_id(self, vmid):
        vms = self.get_vms()
        for vm in vms:
            if vm.id == vmid:
                return vm
        return -1


# callback for creating opennebula users on user login
def user_logged_in_callback(sender, request, user, **kwargs):
    client = oca.Client(settings.OPENNEBULA_USERNAME + ':' + settings.OPENNEBULA_PASSWORD,
                        settings.OPENNEBULA_PROTOCOL + '://' + settings.OPENNEBULA_DOMAIN + ':' + settings.OPENNEBULA_PORT + settings.OPENNEBULA_ENDPOINT)
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
    if find_opennebula_user_by_name(str(user.email), client) == -1:
        user_id = client.call('user.allocate', str(user.email), get_random_password(), 'dummy')
        print("User " + str(user.email) + " does not exist. Created the user. User id = " + str(user_id))


# Finds if an OpenNebula user with user_name exists. Returns the
# OpenNebula user if it exists, -1 otherwise.
def find_opennebula_user_by_name(user_name, client):
    pool = oca.UserPool(client)
    pool.info()
    for user in pool:
        if user.name == user_name:
            return user
    return -1


# Returns random password that is needed by OpenNebula
def get_random_password():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

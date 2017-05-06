import logging
import random
import socket
import string

import oca
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from django.contrib import messages
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.utils.translation import ugettext_lazy as _
from oca.exceptions import OpenNebulaException
from oca.pool import WrongNameError

# Get an instance of a logger
logger = logging.getLogger(__name__)


class HostingManageVMAdmin(admin.ModelAdmin):
    client = None
    oneadmin_client = None

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
    def init_opennebula_client(self, request):
        if self.oneadmin_client is None:
            self.oneadmin_client = oca.Client("{0}:{1}".format(settings.OPENNEBULA_USERNAME,
                                                               settings.OPENNEBULA_PASSWORD),
                                              "{protocol}://{domain}:{port}{endpoint}".format(
                                                  protocol=settings.OPENNEBULA_PROTOCOL,
                                                  domain=settings.OPENNEBULA_DOMAIN,
                                                  port=settings.OPENNEBULA_PORT,
                                                  endpoint=settings.OPENNEBULA_ENDPOINT
                                              ))
            print("{0}:{1}".format(settings.OPENNEBULA_USERNAME,
                                   settings.OPENNEBULA_PASSWORD))
            print("{protocol}://{domain}:{port}{endpoint}".format(
                protocol=settings.OPENNEBULA_PROTOCOL,
                domain=settings.OPENNEBULA_DOMAIN,
                port=settings.OPENNEBULA_PORT,
                endpoint=settings.OPENNEBULA_ENDPOINT
            ))
            self.create_opennebula_user(request)
        if self.client is None:
            opennebula_user = request.user.email
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
            self.init_opennebula_client(request)
            vm_pool = oca.VirtualMachinePool(self.client)
            vm_pool.info()
        except socket.timeout:
            messages.add_message(request, messages.ERROR, _("Socket timeout error."))
        except OpenNebulaException as opennebula_err:
            messages.add_message(request, messages.ERROR, _("OpenNebulaException occurred. {0}".format(opennebula_err)))
        except OSError as err:
            messages.add_message(request, messages.ERROR, "OS error: {0}".format(err))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            vms=vm_pool,
        )
        return TemplateResponse(request, "hosting/managevms.html", context)

    # Function that shows the VMs of the current user
    def show_vms_view(self, request):
        """
            Implemented by Levi for the API
        """ 
        vm_pool = None
        try:
            self.init_opennebula_client(request)
            vm_pool = oca.VirtualMachinePool(self.client)
            vm_pool.info()
        except socket.timeout as socket_err:
            logger.error("Socket timeout error.".format(socket_err))
        except OpenNebulaException as opennebula_err:
            logger.error("OpenNebulaException error: {0}".format(opennebula_err))
        except OSError as os_err:
            logger.error("OSError : {0}".format(os_err))
        except ValueError as value_err:
            logger.error("ValueError : {0}".format(value_err))
        context = dict(
            # Include common variables for rendering the admin template.
            self.admin_site.each_context(request),
            vms=vm_pool,
        )
        return context


    def create_vm_view(self, specs):
        vm_id = None
        try:
            # We do have the vm_template param set. Get and parse it
            # and check it to be in the desired range.
            # We have 8 possible VM templates for the moment which are 1x, 2x, 4x ...
            # the basic template of 10GB disk, 1GB ram, 1 vcpu, 0.1 cpu
            vm_string_formatter = """<VM>
                                      <MEMORY>{memory}</MEMORY>
                                      <VCPU>{vcpu}</VCPU>
                                      <CPU>{cpu}</CPU>
                                      <DISK>
                                        <TYPE>{disk_type}</TYPE>
                                        <SIZE>{size}</SIZE>
                                      </DISK>
                                    </VM>
                                    """
            vm_id = oca.VirtualMachine.allocate(
                self.client,
                vm_string_formatter.format(
                    memory=1024 * specs.get('memory'),
                    vcpu=specs.get('cores'),
                    cpu=0.1 * specs.get('cores'),
                    disk_type='fs',
                    size=10000 * specs.get('disk_size')
                )
            )
                # message = _("Created with id = " + str(vm_id))
                # messages.add_message(request, messages.SUCCESS, message)
        except socket.timeout as socket_err:
            logger.error("Socket timeout error: {0}".format(socket_err))
        except OpenNebulaException as opennebula_err:
            logger.error("OpenNebulaException error: {0}".format(opennebula_err))
        except OSError as os_err:
            logger.error("OSError : {0}".format(os_err))
        except ValueError as value_err:
            logger.error("ValueError : {0}".format(value_err))

        return vm_id



    # Creating VM by using method allocate(client, template)
    def create_vm(self, request):
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
                    vm_string_formatter = """<VM>
                                              <MEMORY>{memory}</MEMORY>
                                              <VCPU>{vcpu}</VCPU>
                                              <CPU>{cpu}</CPU>
                                              <DISK>
                                                <TYPE>{disk_type}</TYPE>
                                                <SIZE>{size}</SIZE>
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
                    message = _("Created with id = " + str(vm_id))
                    messages.add_message(request, messages.SUCCESS, message)
                else:
                    messages.add_message(request, messages.ERROR,
                                         _("Please select an appropriate value for vm template."))
            except socket.timeout as socket_err:
                messages.add_message(request, messages.ERROR, _("Socket timeout error."))
                logger.error("Socket timeout error: {0}".format(socket_err))
            except OpenNebulaException as opennebula_err:
                messages.add_message(request, messages.ERROR,
                                     _("OpenNebulaException occurred. {0}".format(opennebula_err)))
                logger.error("OpenNebulaException error: {0}".format(opennebula_err))
            except OSError as os_err:
                messages.add_message(request, messages.ERROR, _("OS error: {0}".format(os_err)))
                logger.error("OSError : {0}".format(os_err))
            except ValueError as value_err:
                messages.add_message(request, messages.ERROR,
                                     _("Please select an appropriate value for vm template."))
                logger.error("ValueError : {0}".format(value_err))
        return redirect('admin:showvms')

    # Delete VM from the pool and DB by using method finalize()
    def delete_vm(self, request, vmid):
        vm_id = int(vmid)
        # get the desired vm from the pool
        logger.debug("Deleting vm with id {0}".format(vm_id))
        vm = self.get_vm_by_id(vm_id)
        if vm is None:
            messages.add_message(request, messages.ERROR, _("Did not find a vm with id = {0}".format(vm_id)))
        else:
            logger.debug("Deleting vm_id = " + str(vm_id) + " state = " + vm.str_state)
            if vm.str_state == 'PENDING' or vm.str_state == 'POWEROFF' or vm.str_state == 'ACTIVE':
                vm.delete()
                messages.add_message(request, messages.SUCCESS,
                                     _("Deleted from {0} state vm with id = {1}".format(vm.str_state, str(vm_id))))
            else:
                vm.finalize()
                messages.add_message(request, messages.SUCCESS,
                                     _("Deleted (using finalize()) from {0} state vm with id = {1}".format(vm.str_state,
                                                                                                           str(vm_id))))
        return redirect('admin:showvms')

    def stop_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm is None:
            messages.add_message(request, messages.ERROR, _("Did not find a vm with id = {0}", vm_id))
        else:
            vm.stop()
            messages.add_message(request, messages.SUCCESS, _("Stopped the vm with id = {0}", vm_id))
        return redirect('admin:showvms')

    def start_vm(self, request, vmid):
        vm_id = int(vmid)
        vm = self.get_vm_by_id(vm_id)
        if vm is None:
            messages.add_message(request, messages.ERROR, _("Did not find a vm with id = {0}", vm_id))
        else:
            vm.resume()
            messages.add_message(request, messages.SUCCESS, _("Started the vm with id = {0}", vm_id))
        return redirect('admin:showvms')

    # Retrives virtual machine pool information
    def get_vm_pool(self):
        vm_pool = oca.VirtualMachinePool(self.client)
        vm_pool.info()
        return vm_pool

    def get_vm_by_id(self, vmid):
        vm_pool = self.get_vm_pool()
        return vm_pool.get_by_id(vmid)

    def create_opennebula_user(self, request):
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
        #     4. If the user's email is not registered with OpenNebula,
        #     WrongNameError is raised. We create an OpenNebula user in 
        #     such case.
        try:
            user_pool = oca.UserPool(self.oneadmin_client)
            user_pool.info()
            opennebula_user = user_pool.get_by_name(request.user.email)
            logger.debug("User {0} exists. User id = {1}".format(request.user.email, opennebula_user.id))
        except WrongNameError as wrong_name_err:
            user_id = self.oneadmin_client.call('user.allocate', request.user.email, get_random_password(),
                                                'dummy')
            logger.debug("User {0} does not exist. Created the user. User id = {1}", request.user.email, user_id)
        except OpenNebulaException as err:
            messages.add_message(request, messages.ERROR,
                                 "Error : {0}".format(err))
            logger.error("Error : {0}".format(err))


# Returns random password that is needed by OpenNebula
def get_random_password():
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(20))

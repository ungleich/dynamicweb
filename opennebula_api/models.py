import oca
import socket
import logging


from django.conf import settings
from django.utils.functional import cached_property

from oca.pool import WrongNameError
from oca.exceptions import OpenNebulaException
logger = logging.getLogger(__name__)

class OpenNebulaManager():
    """This class represents an opennebula manager."""

    def __init__(self, email=None, password=None, create_user=True):
        
        # Get oneadmin client
        self.oneadmin_client = self._get_opennebula_client(
            settings.OPENNEBULA_USERNAME,
            settings.OPENNEBULA_PASSWORD
        )
        
        if not create_user or email is None:
            return

        # Get or create oppenebula user using given credentials
        self.opennebula_user = self._get_or_create_user(
            email,
            password
        )

        # If opennebula user was created/obtained, get his client
        if self.opennebula_user:
            self.client = self._get_opennebula_client(
                email,
                password
            )

    def _get_opennebula_client(self, username, password):
        return oca.Client("{0}:{1}".format(
            username,
            password),
            "{protocol}://{domain}:{port}{endpoint}".format(
                protocol=settings.OPENNEBULA_PROTOCOL,
                domain=settings.OPENNEBULA_DOMAIN,
                port=settings.OPENNEBULA_PORT,
                endpoint=settings.OPENNEBULA_ENDPOINT
        ))

    def _get_or_create_user(self, email, password):
        try:
            user_pool = self._get_user_pool()
            opennebula_user = user_pool.get_by_name(email)
            return opennebula_user
        except WrongNameError as wrong_name_err:
            opennebula_user = self.oneadmin_client.call(oca.User.METHODS['allocate'], email,
                                                        password, 'core')
            return opennebula_user
        #TODO: Replace with logger
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
    def _get_user_pool(self):
        try:
            user_pool = oca.UserPool(self.oneadmin_client)
            user_pool.info()
        #TODO: Replace with logger
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
        return user_pool

    def _get_vm_pool(self):
        try:
            vm_pool = oca.VirtualMachinePool(self.client)
            vm_pool.info()
        except AttributeError:
            print('Could not connect via client, using oneadmin instead') 
            vm_pool = oca.VirtualMachinePool(self.oneadmin_client)
            vm_pool.info(filter=-2)

        #TODO: Replace with logger
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
        return vm_pool

    def get_vms(self):
        return self._get_vm_pool()
   
    def get_vm(self, vm_id):
        vm_pool = self._get_vm_pool()
        return vm_pool.get_by_id(int(vm_id))

    #TODO: get app with id 
    def create_vm(self, template_id, app_id=None, ssh_key=None):
        extra_template = "<CONTEXT><SSH_PUBLIC_KEY>{ssh_key}</SSH_PUBLIC_KEY></CONTEXT>".format(
            ssh_key=ssh_key
        )
        vm_id = self.oneadmin_client.call(
            oca.VmTemplate.METHODS['instantiate'],
            template_id,
            '',
            False,
            extra_template
        )
        try:
            self.oneadmin_client.call(
                oca.VirtualMachine.METHODS['chown'],
                vm_id,
                self.opennebula_user.id,
                self.opennebula_user.group_ids[0]
            )
        except AttributeError:
            print('Could not change owner, opennebula_user is not set.')
        return vm_id

    def delete_vm(self, vm_id):
        TERMINATE_ACTION = 'terminate'
        vm_terminated = False
        try:
            self.oneadmin_client.call(
                oca.VirtualMachine.METHODS['action'],
                TERMINATE_ACTION,
                int(vm_id),
            )
            vm_terminated = True
        except socket.timeout as socket_err:
            logger.info("Socket timeout error: {0}".format(socket_err))
            print("Socket timeout error: {0}".format(socket_err))
        except OpenNebulaException as opennebula_err:
            logger.info("OpenNebulaException error: {0}".format(opennebula_err))
            print("OpenNebulaException error: {0}".format(opennebula_err))
        except OSError as os_err:
            logger.info("OSError : {0}".format(os_err))
            print("OSError : {0}".format(os_err))
        except ValueError as value_err:
            logger.info("ValueError : {0}".format(value_err))
            print("ValueError : {0}".format(value_err))

        return vm_terminated

    def _get_template_pool(self):
        try:
           template_pool = oca.VmTemplatePool(self.oneadmin_client)
           template_pool.info()
        #TODO: Replace with logger
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
        return template_pool

    def get_templates(self):
        public_templates = [
                template 
                for template in self._get_template_pool()
                if 'public-' in template.name 
                ]
        return public_templates 
    def get_template(self, template_id):
        template_pool = self._get_template_pool()
        return template_pool.get_by_id(template_id)

    
    
    def create_template(self, name, cores, memory, disk_size, core_price, memory_price,
                        disk_size_price, ssh='' ):
        """Create and add a new template to opennebula.
        :param name:      A string representation describing the template.
                          Used as label in view.
        :param cores:     Amount of virtual cpu cores for the VM.
        :param memory:  Amount of RAM for the VM (GB)
        :param disk_size:    Amount of disk space for VM (GB)
        :param core_price:     Price of virtual cpu for the VM per core.
        :param memory_price:  Price of RAM for the VM per GB
        :param disk_size_price:    Price of disk space for VM per GB
        :param ssh: User public ssh key
        """
        template_string_formatter = """<TEMPLATE>
                                        <NAME>{name}</NAME>
                                        <MEMORY>{memory}</MEMORY>
                                        <VCPU>{vcpu}</VCPU>
                                        <CPU>{cpu}</CPU>
                                        <DISK>
                                         <TYPE>fs</TYPE>
                                         <SIZE>{size}</SIZE>
                                         <DEV_PREFIX>vd</DEV_PREFIX>
                                        </DISK>
                                        <CPU_COST>{cpu_cost}</CPU_COST>
                                        <MEMORY_COST>{memory_cost}</MEMORY_COST>
                                        <DISK_COST>{disk_cost}</DISK_COST>
                                        <SSH_PUBLIC_KEY>{ssh}</SSH_PUBLIC_KEY>
                                       </TEMPLATE>
                                       """
        template_id = oca.VmTemplate.allocate(
            self.oneadmin_client,
            template_string_formatter.format(
                name=name,
                vcpu=cores,
                cpu=0.1*cores,
                size=1024 * disk_size,
                memory=1024 * memory,
                # * 10 because we set cpu to *0.1
                cpu_cost=10*core_price,
                memory_cost=memory_price,
                disk_cost=disk_size_price,
                ssh=ssh
            )
        )

        return template_id

    def delete_template(self, template_id):
        self.oneadmin_client.call(oca.VmTemplate.METHODS['delete'], template_id, False)


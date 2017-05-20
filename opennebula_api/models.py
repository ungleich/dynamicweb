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

    def __init__(self, email=None, password=None):
        
        # Get oneadmin client
        self.oneadmin_client = self._get_opennebula_client(
            settings.OPENNEBULA_USERNAME,
            settings.OPENNEBULA_PASSWORD
        )
        
        # Get or create oppenebula user using given credentials
        try:
            self.opennebula_user = self._get_or_create_user(
                email,
                password
            )
            # If opennebula user was created/obtained, get his client
            self.client = self._get_opennebula_client(
                email,
                password
            )
        except:
            pass

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
            logger.debug(
                 "User {0} does not exist. Created the user. User id = {1}",
                 email,
                 opennebula_user
             )
            return opennebula_user
        except ConnectionRefusedError:
            logger.info('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
    def _get_user_pool(self):
        try:
            user_pool = oca.UserPool(self.oneadmin_client)
            user_pool.info()
        except ConnectionRefusedError:
            logger.info('Could not connect to host: {host} via protocol {protocol}'.format(
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
            logger.info('Could not connect via client, using oneadmin instead') 
            try:
                vm_pool = oca.VirtualMachinePool(self.oneadmin_client)
                vm_pool.info(filter=-2)
                return vm_pool
            except:
                raise ConnectionRefusedError

        except ConnectionRefusedError:
            logger.info('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
        # For now we'll just handle all other errors as connection errors
        except:
            raise ConnectionRefusedError

    def get_vms(self):
        try:
            return self._get_vm_pool()
        except ConnectionRefusedError:
            raise ConnectionRefusedError
            
   
    def get_vm(self, vm_id):
        vm_id = int(vm_id)
        try:
            vm_pool = self._get_vm_pool()
            return vm_pool.get_by_id(vm_id)
        except:
            raise ConnectionRefusedError

    def create_vm(self, template_id, specs, ssh_key=None):

        template = self.get_template(template_id)
        vm_specs_formatter = """<TEMPLATE>
                                 <MEMORY>{memory}</MEMORY>
                                 <VCPU>{vcpu}</VCPU>
                                 <CPU>{cpu}</CPU>
                                 <CONTEXT>
                                  <SSH_PUBLIC_KEY>{ssh}</SSH_PUBLIC_KEY>
                                 </CONTEXT>
                           """
        try:
            disk = template.template.disks[0]
            image_id = disk.image_id
            vm_specs = vm_specs_formatter.format(
                                        vcpu=int(specs['cpu']),
                                        cpu=0.1* int(specs['cpu']),
                                        memory=1024 * int(specs['memory']),
                                        ssh=ssh_key
                    
                    )
            vm_specs += """<DISK>
                                  <TYPE>fs</TYPE>
                                  <SIZE>{size}</SIZE>
                                  <DEV_PREFIX>vd</DEV_PREFIX>
                                  <IMAGE_ID>{image_id}</IMAGE_ID>
                           </DISK>
                          </TEMPLATE>
                        """.format(size=1024 * int(specs['disk_size']),
                                   image_id=image_id)

        except:
            disk = template.template.disks[0]
            image = disk.image
            image_uname = disk.image_uname

            vm_specs = vm_specs_formatter.format(
                                        vcpu=int(specs['cpu']),
                                        cpu=0.1* int(specs['cpu']),
                                        memory=1024 * int(specs['memory']),
                                        ssh=ssh_key
                    
                    )
            vm_specs += """<DISK>
                                  <TYPE>fs</TYPE>
                                  <SIZE>{size}</SIZE>
                                  <DEV_PREFIX>vd</DEV_PREFIX>
                                  <IMAGE>{image}</IMAGE>
                                  <IMAGE_UNAME>{image_uname}</IMAGE_UNAME>
                           </DISK>
                          </TEMPLATE>
                        """.format(size=1024 * int(specs['disk_size']),
                                   image=image,
                                   image_uname=image_uname)
        vm_id = template.instantiate(name ='',
                                    pending=False,
                                    extra_template=vm_specs,                                    )

        try:
            self.oneadmin_client.call(
                oca.VirtualMachine.METHODS['chown'],
                vm_id,
                self.opennebula_user.id,
                self.opennebula_user.group_ids[0]
            )
        except AttributeError:
            logger.info('Could not change owner for vm with id: {}.'.format(vm_id))
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
        except OpenNebulaException as opennebula_err:
            logger.info("OpenNebulaException error: {0}".format(opennebula_err))
        except OSError as os_err:
            logger.info("OSError : {0}".format(os_err))
        except ValueError as value_err:
            logger.info("ValueError : {0}".format(value_err))

        return vm_terminated

    def _get_template_pool(self):
        try:
           template_pool = oca.VmTemplatePool(self.oneadmin_client)
           template_pool.info()
           return template_pool
        except ConnectionRefusedError:
            logger.info('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            raise ConnectionRefusedError
        except:
            raise ConnectionRefusedError
        

    def get_templates(self):
        try:
            public_templates = [
                    template 
                    for template in self._get_template_pool()
                    if 'public-' in template.name 
                    ]
            return public_templates 
        except ConnectionRefusedError:
            raise ConnectionRefusedError
        except:
            raise ConnectionRefusedError

    def try_get_templates(self):
        try:
            return self.get_templates()
        except:
            return []

    def get_template(self, template_id):
        template_id = int(template_id)
        try:
            template_pool = self._get_template_pool()
            return template_pool.get_by_id(template_id)
        except:
            raise ConnectionRefusedError

    def change_user_password(self, new_password):
        self.oneadmin_client.call(
            oca.User.METHODS['passwd'],
            self.opennebula_user.id,
            new_password
        ) 

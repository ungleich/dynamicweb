import logging
import socket

import oca
from django.conf import settings
from oca.exceptions import OpenNebulaException
from oca.pool import WrongNameError, WrongIdError

from hosting.models import HostingOrder
from utils.models import CustomUser
from utils.tasks import save_ssh_key, save_ssh_key_error_handler
from .exceptions import KeyExistsError, UserExistsError, UserCredentialError

logger = logging.getLogger(__name__)


class OpenNebulaManager():
    """This class represents an opennebula manager."""

    def __init__(self, email=None, password=None):
        self.email = email
        self.password = password
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

    def _get_client(self, user):
        """Get a opennebula client object for a CustomUser object

        Args:
            user (CustomUser): dynamicweb CustomUser object

        Returns:
            oca.Client: Opennebula client object

        Raise:
            ConnectionError: If the connection to the opennebula server can't be
                established
        """
        return self._get_opennebula_client(user.email, user.password)

    def _get_opennebula_client(self, username, password):
        return oca.Client(
            "{0}:{1}".format(username, password),
            "{protocol}://{domain}:{port}{endpoint}".format(
                protocol=settings.OPENNEBULA_PROTOCOL,
                domain=settings.OPENNEBULA_DOMAIN,
                port=settings.OPENNEBULA_PORT,
                endpoint=settings.OPENNEBULA_ENDPOINT
            )
        )

    def _get_user(self, user):
        """Get the corresponding opennebula user for a CustomUser object

        Args:
            user (CustomUser): dynamicweb CustomUser object

        Returns:
            oca.User: Opennebula user object

        Raise:
            WrongNameError: If no openebula user with this credentials exists
            ConnectionError: If the connection to the opennebula server can't be
                established
        """
        user_pool = self._get_user_pool()
        return user_pool.get_by_name(user.email)

    def create_user(self, user: CustomUser):
        """Create a new opennebula user or a corresponding CustomUser object


        Args:
            user (CustomUser): dynamicweb CustomUser object

        Returns:
            int: Return the opennebula user id

        Raises:
            ConnectionError: If the connection to the opennebula server can't be
                established
            UserExistsError: If a user with this credeintals already exits on the
                server
            UserCredentialError: If a user with this email exists but the
                password is worng

        """
        try:
            self._get_user(user)
            try:
                self._get_client(self, user)
                logger.debug('User already exists')
                raise UserExistsError()
            except OpenNebulaException as err:
                logger.error('OpenNebulaException error: {0}'.format(err))
                logger.debug('User exists but password is wrong')
                raise UserCredentialError()

        except WrongNameError:
            user_id = self.oneadmin_client.call(oca.User.METHODS['allocate'],
                                                user.email, user.password,
                                                'core')
            logger.debug(
                'Created a user for CustomObject: {user} with user id = {u_id}',
                user=user,
                u_id=user_id
            )
            return user_id
        except ConnectionRefusedError:
            logger.error(
                'Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
            )
            raise ConnectionRefusedError

    def _get_or_create_user(self, email, password):
        try:
            user_pool = self._get_user_pool()
            opennebula_user = user_pool.get_by_name(email)
            return opennebula_user
        except WrongNameError as wrong_name_err:
            opennebula_user = self.oneadmin_client.call(
                oca.User.METHODS['allocate'], email,
                password, 'core')
            logger.debug(
                "User {} does not exist. Created the user. User id = {}".format(
                    email,
                    opennebula_user
                )
            )
            return opennebula_user
        except ConnectionRefusedError:
            logger.info(
                'Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
            )
            raise ConnectionRefusedError

    def _get_user_pool(self):
        try:
            user_pool = oca.UserPool(self.oneadmin_client)
            user_pool.info()
        except ConnectionRefusedError:
            logger.info(
                'Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
            )
            raise
        return user_pool

    def _get_vm_pool(self):
        try:
            vm_pool = oca.VirtualMachinePool(self.client)
            vm_pool.info()
            return vm_pool
        except AttributeError:
            logger.info('Could not connect via client, using oneadmin instead')
            try:
                vm_pool = oca.VirtualMachinePool(self.oneadmin_client)
                vm_pool.info(filter=-2)
                return vm_pool
            except:
                raise ConnectionRefusedError

        except ConnectionRefusedError:
            logger.info(
                'Could not connect to host: {host} via protocol {protocol}'.format(
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
        except WrongIdError:
            raise WrongIdError
        except:
            raise ConnectionRefusedError

    def get_ipv6(self, vm_id):
        """
        Returns the first IPv6 of the given vm.

        :return: An IPv6 address string, if it exists else returns None
        """
        ipv6_list = self.get_all_ipv6_addresses(vm_id)
        if len(ipv6_list) > 0:
            return ipv6_list[0]
        else:
            return None

    def get_all_ipv6_addresses(self, vm_id):
        """
        Returns a list of IPv6 addresses of the given vm

        :param vm_id: The ID of the vm
        :return:
        """
        ipv6_list = []
        vm = self.get_vm(vm_id)
        for nic in vm.template.nics:
            if hasattr(nic, 'ip6_global'):
                ipv6_list.append(nic.ip6_global)
        return ipv6_list

    def create_vm(self, template_id, specs, ssh_key=None, vm_name=None):

        template = self.get_template(template_id)
        vm_specs_formatter = """<TEMPLATE>
                                 <MEMORY>{memory}</MEMORY>
                                 <VCPU>{vcpu}</VCPU>
                                 <CPU>{cpu}</CPU>
                             """
        try:
            disk = template.template.disks[0]
            image_id = disk.image_id
            vm_specs = vm_specs_formatter.format(
                vcpu=int(specs['cpu']),
                cpu=0.1 * int(specs['cpu']),
                memory=1024 * int(specs['memory']),

            )
            vm_specs += """<DISK>
                                  <TYPE>fs</TYPE>
                                  <SIZE>{size}</SIZE>
                                  <DEV_PREFIX>vd</DEV_PREFIX>
                                  <IMAGE_ID>{image_id}</IMAGE_ID>
                           </DISK>
                        """.format(size=1024 * int(specs['disk_size']),
                                   image_id=image_id)

        except:
            disk = template.template.disks[0]
            image = disk.image
            image_uname = disk.image_uname

            vm_specs = vm_specs_formatter.format(
                vcpu=int(specs['cpu']),
                cpu=0.1 * int(specs['cpu']),
                memory=1024 * int(specs['memory']),

            )
            vm_specs += """<DISK>
                                  <TYPE>fs</TYPE>
                                  <SIZE>{size}</SIZE>
                                  <DEV_PREFIX>vd</DEV_PREFIX>
                                  <IMAGE>{image}</IMAGE>
                                  <IMAGE_UNAME>{image_uname}</IMAGE_UNAME>
                           </DISK>
                        """.format(size=1024 * int(specs['disk_size']),
                                   image=image,
                                   image_uname=image_uname)

        vm_specs += "<CONTEXT>"
        if ssh_key:
            vm_specs += "<SSH_PUBLIC_KEY>{ssh}</SSH_PUBLIC_KEY>".format(
                ssh=ssh_key)
        vm_specs += """<NETWORK>YES</NETWORK>
                   </CONTEXT>
                </TEMPLATE>
                """
        try:
            vm_id = self.client.call(
                oca.VmTemplate.METHODS['instantiate'], template.id, '', True,
                vm_specs, False
            )
        except OpenNebulaException as err:
            logger.error("OpenNebulaException: {0}".format(err))
            return None

        self.oneadmin_client.call(
            oca.VirtualMachine.METHODS['action'],
            'release',
            vm_id
        )

        if vm_name is not None:
            self.oneadmin_client.call(
                'vm.rename',
                vm_id,
                vm_name
            )
        return vm_id

    def delete_vm(self, vm_id):
        TERMINATE_ACTION = 'terminate-hard'
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
            logger.info(
                "OpenNebulaException error: {0}".format(opennebula_err))
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
            logger.info(
                """Could not connect to host: {host} via protocol
                 {protocol}""".format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
            )
            raise ConnectionRefusedError
        except:
            raise ConnectionRefusedError

    def get_templates(self, prefix='public-'):
        try:
            public_templates = [
                template
                for template in self._get_template_pool()
                if template.name.startswith(prefix)
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

    def create_template(self, name, cores, memory, disk_size, core_price,
                        memory_price,
                        disk_size_price, ssh=''):
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
                cpu=0.1 * cores,
                size=1024 * disk_size,
                memory=1024 * memory,
                # * 10 because we set cpu to *0.1
                cpu_cost=10 * core_price,
                memory_cost=memory_price,
                disk_cost=disk_size_price,
                ssh=ssh
            )
        )

        return template_id

    def delete_template(self, template_id):
        self.oneadmin_client.call(
            oca.VmTemplate.METHODS['delete'], template_id, False
        )

    def change_user_password(self, passwd_hash):
        self.oneadmin_client.call(
            oca.User.METHODS['passwd'],
            self.opennebula_user.id,
            passwd_hash
        )

    def add_public_key(self, user, public_key='', merge=False):
        """

        Args:
            user (CustomUser): Dynamicweb user
            public_key (string): Public key to add to the user
            merge (bool): Optional if True the new public key replaces the old

        Raises:
            KeyExistsError: If replace is False and the user already has a
                public key
            WrongNameError: If no openebula user with this credentials exists
            ConnectionError: If the connection to the opennebula server can't be
                established

        Returns:
            True if public_key was added

        """
        # TODO: Check if we can remove this first try because we basically just
        # raise the possible Errors
        try:
            open_user = self._get_user(user)
            try:
                old_key = open_user.template.ssh_public_key
                if not merge:
                    raise KeyExistsError()
                public_key += '\n{key}'.format(key=old_key)

            except AttributeError:
                pass
            self.oneadmin_client.call('user.update', open_user.id,
                                      '<CONTEXT><SSH_PUBLIC_KEY>{key}</SSH_PUBLIC_KEY></CONTEXT>'
                                      .format(key=public_key))
            return True
        except WrongNameError:
            raise

        except ConnectionError:
            raise

    def remove_public_key(self, user, public_key=''):
        """

        Args:
            user (CustomUser): Dynamicweb user
            public_key (string): Public key to be removed to the user

        Raises:
            KeyDoesNotExistsError: If replace is False and the user already has a
                public key
            WrongNameError: If no openebula user with this credentials exists
            ConnectionError: If the connection to the opennebula server can't be
                established

        Returns:
            True if public_key was removed

        """

        try:
            open_user = self._get_user(user)
            try:
                old_key = open_user.template.ssh_public_key
                if public_key not in old_key:
                    return False
                    # raise KeyDoesNotExistsError()
                if '\n{}'.format(public_key) in old_key:
                    public_key = old_key.replace('\n{}'.format(public_key), '')
                else:
                    public_key = old_key.replace(public_key, '')

            except AttributeError:
                return False
                # raise KeyDoesNotExistsError()

            self.oneadmin_client.call('user.update', open_user.id,
                                      '<CONTEXT><SSH_PUBLIC_KEY>{key}</SSH_PUBLIC_KEY></CONTEXT>'
                                      .format(key=public_key))
            return True
        except WrongNameError:
            raise

        except ConnectionError:
            raise

    def manage_public_key(self, keys, hosts=None, countdown=0):
        """
        A function that manages the supplied keys in the
        authorized_keys file of the given list of hosts. If hosts
        parameter is not supplied, all hosts of this customer
        will be configured with the supplied keys

        :param keys: A list of ssh keys that are to be added/removed
                     A key should be a dict of the form
                     {
                       'value': 'sha-.....', # public key as string
                       'state': True         # whether key is to be added or
                     }                       # removed
        :param hosts: A list of hosts IPv6 addresses
        :param countdown: Parameter to be passed to celery apply_async
               Allows to delay a task by `countdown` number of seconds
        :return:
        """
        if hosts is None:
            hosts = self.get_all_hosts()

        if len(hosts) > 0 and len(keys) > 0:
            save_ssh_key.apply_async((hosts, keys), countdown=countdown,
                                     link_error=save_ssh_key_error_handler.s())
        else:
            logger.debug(
                "Keys and/or hosts are empty, so not managing any keys"
            )

    def get_all_hosts(self):
        """
        A utility function to obtain all hosts of this owner
        :return: A list of IPv6 addresses of all the hosts of this customer or
                an empty list if none exist
        """
        owner = CustomUser.objects.filter(
            email=self.email).first()
        all_orders = HostingOrder.objects.filter(customer__user=owner)
        hosts = []
        if len(all_orders) > 0:
            logger.debug("The user {} has 1 or more VMs. We need to configure "
                         "the ssh keys.".format(self.email))
            for order in all_orders:
                try:
                    ip = self.get_ipv6(order.vm_id)
                    hosts.append(ip)
                except WrongIdError:
                    logger.debug(
                        "VM with ID {} does not exist".format(order.vm_id))
        else:
            logger.debug("The user {} has no VMs. We don't need to configure "
                         "the ssh keys.".format(self.email))
        return hosts

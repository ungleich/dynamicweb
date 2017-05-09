import oca
import socket

from django.db import models
from django.conf import settings

from oca.pool import WrongNameError

class VirtualMachineTemplate(models.Model):
    """This class represents an opennebula template."""
    opennebula_id = models.IntegerField()
    base_price = models.FloatField()
    memory_price = models.FloatField()
    core_price = models.FloatField()
    disk_size_price = models.FloatField()


class VirtualMachine(models.Model):
    """This class represents an opennebula virtual machine."""
    opennebula_id = models.IntegerField()
    template = models.ForeignKey(VirtualMachineTemplate)

class OpenNebulaManager():
    """This class represents an opennebula manager."""

    def __init__(self, email=None, password=None, create_user=True):
        
        # Get oneadmin client
        self.oneadmin_client = self._get_opennebula_client(
            settings.OPENNEBULA_USERNAME,
            settings.OPENNEBULA_PASSWORD
        )
        

        if not create_user:
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
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
            return opennebula_user
    def _get_user_pool(self):
        try:
            user_pool = oca.UserPool(self.oneadmin_client)
            user_pool.info()
        except ConnectionRefusedError:
            print('Could not connect to host: {host} via protocol {protocol}'.format(
                    host=settings.OPENNEBULA_DOMAIN,
                    protocol=settings.OPENNEBULA_PROTOCOL)
                )
        return user_pool
    def create_template(self, name, cores, memory, disk_size):
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
                                       </TEMPLATE>
                                       """
        template_id = oca.VmTemplate.allocate(
            self.oneadmin_client,
            template_string_formatter.format(
                name=name,
                vcpu=cores,
                cpu=0.1*cores,
                size=1024 * disk_size,
                memory=1024 * memory
            )
        )

        return template_id

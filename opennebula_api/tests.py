import random
import string

from django.conf import settings
from django.test import TestCase
from unittest import skipIf

from .models import OpenNebulaManager
from .serializers import VirtualMachineSerializer
from utils.models import CustomUser


@skipIf(
    settings.OPENNEBULA_DOMAIN is None or
    settings.OPENNEBULA_DOMAIN == "test_domain",
    """OpenNebula details unavailable, so skipping
     OpenNebulaManagerTestCases"""
)
class OpenNebulaManagerTestCases(TestCase):
    """This class defines the test suite for the opennebula manager model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.email = '{}@ungleich.ch'.format(''.join(random.choices(string.ascii_uppercase, k=10)))
        self.password = ''.join(random.choices(string.ascii_uppercase + string.digits, k=20))

        self.user = CustomUser.objects.create(name='test', email=self.email,
                                              password=self.password)

        self.vm_specs = {}
        self.vm_specs['cpu'] = 1
        self.vm_specs['memory'] = 2
        self.vm_specs['disk_size'] = 10

        self.manager = OpenNebulaManager()

    def test_connect_to_server(self):
        """Test the opennebula manager can connect to a server."""
        try:
            ver = self.manager.oneadmin_client.version()
        except:
            ver = None
        self.assertTrue(ver is not None)

    def test_get_user(self):
        """Test the opennebula manager can get a existing user."""
        self.manager.create_user(self.user)
        user = self.manager._get_user(self.user)
        name = user.name
        self.assertNotEqual(name, None)

    def test_create_and_delete_user(self):
        """Test the opennebula manager can create and delete a new user."""
        old_count = len(self.manager._get_user_pool())
        self.manager = OpenNebulaManager(email=self.email,
                                         password=self.password)
        user_pool = self.manager._get_user_pool()
        new_count = len(user_pool)
        # Remove the user afterwards
        user = user_pool.get_by_name(self.email)
        user.delete()

        self.assertNotEqual(old_count, new_count)

    def test_user_can_login(self):
        """ Test the manager can login to a new created user"""
        self.manager.create_user(self.user)
        user = self.manager._get_user(self.user)
        client = self.manager._get_client(self.user)
        version = client.version()

        # Cleanup
        user.delete()
        self.assertNotEqual(version, None)

    def test_add_public_key_to_user(self):
        """ Test the manager can add a new public key to an user """
        self.manager.create_user(self.user)
        user = self.manager._get_user(self.user)
        public_key = 'test'
        self.manager.add_public_key(self.user, public_key)
        # Fetch new user information from opennebula
        user.info()
        user_public_key = user.template.ssh_public_key
        # Cleanup
        user.delete()

        self.assertEqual(user_public_key, public_key)

    def test_append_public_key_to_user(self):
        """ Test the manager can append a new public key to an user """
        self.manager.create_user(self.user)
        user = self.manager._get_user(self.user)
        public_key = 'test'
        self.manager.add_public_key(self.user, public_key)
        # Fetch new user information from opennebula
        user.info()
        old_public_key = user.template.ssh_public_key
        self.manager.add_public_key(self.user, public_key, merge=True)
        user.info()
        new_public_key = user.template.ssh_public_key
        # Cleanup
        user.delete()

        self.assertEqual(new_public_key, '{}\n{}'.format(old_public_key,
                                                         public_key))

    def test_remove_public_key_to_user(self):
        """ Test the manager can remove a public key from an user """
        self.manager.create_user(self.user)
        user = self.manager._get_user(self.user)
        public_key = 'test'
        self.manager.add_public_key(self.user, public_key)
        self.manager.add_public_key(self.user, public_key, merge=True)
        user.info()
        old_public_key = user.template.ssh_public_key
        self.manager.remove_public_key(self.user, public_key)
        user.info()
        new_public_key = user.template.ssh_public_key
        # Cleanup
        user.delete()

        self.assertEqual(new_public_key,
                         old_public_key.replace('{}\n'.format(public_key), '', 1))

    def test_requires_ssh_key_for_new_vm(self):
        """Test the opennebula manager requires the user to have a ssh key when
        creating a new vm"""


@skipIf(
    settings.OPENNEBULA_DOMAIN is None or
    settings.OPENNEBULA_DOMAIN == "test_domain",
    """OpenNebula details unavailable, so skipping
     VirtualMachineSerializerTestCase"""
)
class VirtualMachineSerializerTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.manager = OpenNebulaManager(email=None, password=None)

    def test_serializer_strips_of_public(self):
        """ Test the serialized virtual machine object contains no
        'public-'."""

        for vm in self.manager.get_vms():
            serialized = VirtualMachineSerializer(vm)
            self.assertEqual(serialized.data.get('name'), vm.name.strip('public-'))
            break

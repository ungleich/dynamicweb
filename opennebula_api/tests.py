from django.test import TestCase
from .models import VirtualMachine, VirtualMachineTemplate, OpenNebulaManager

class OpenNebulaManagerTestCases(TestCase):
    """This class defines the test suite for the opennebula manager model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.cores = 1 
        self.memory = 1
        self.disk_size = 10.0
        
        self.email = 'test@test.com'
        self.password = 'testtest'

        self.manager = OpenNebulaManager(email=None, password=None, create_user=False) 


    def test_model_can_connect_to_server(self):
        """Test the opennebula manager model can connect to a server."""
        self.assertFalse(self.manager is None)

    def test_model_can_create_user(self):
        """Test the opennebula manager model can create a new user."""
        old_count = len(self.manager._get_user_pool())
        self.manager = OpenNebulaManager(email=self.email,
                                         password=self.password,
                                         create_user=True)
        new_count = len(self.manager._get_user_pool())
        self.assertNotEqual(old_count, new_count)


class VirtualMachineTemplateTestCase(TestCase):
    """This class defines the test suite for the virtualmachine template model."""

    def setUp(self):
        """Define the test client and other test variables."""
        self.template_name = "Standard"
        self.base_price = 0.0
        self.core_price = 5.0
        self.memory_price = 2.0
        self.disk_size_price = 0.6

        self.cores = 1 
        self.memory = 1
        self.disk_size = 10.0

        self.manager = OpenNebulaManager(email=None, password=None, create_user=False)
        self.opennebula_id = self.manager.create_template(self.cores, self.memory,
                                                          self.disk_size)

        self.template = VirtualMachineTemplate(opennebula_id=self.opennebula_id,
                                               base_price=self.base_price,
                                               memory_price=self.memory_price,
                                               core_price=self.core_price,
                                               disk_size_price=self.disk_size_price)


    def test_model_can_create_a_virtualmachine_template(self):
        """Test the virtualmachine template model can create a template."""
        old_count = VirtualMachineTemplate.objects.count()
        self.template.save()
        new_count = VirtualMachineTemplate.objects.count()
        self.assertNotEqual(old_count, new_count)


class VirtualMachineTestCase(TestCase):
    def setUp(self):
        """Define the test client and other test variables."""
        self.manager = OpenNebulaManager(email=None, password=None, create_user=False) 
        self.template = VirtualMachineTemplate.objects.first()
        self.template_id = self.template.opennebula_id()
        self.opennebula_id = self.manager.create_virtualmachine(template_id=self.template_id)
                                           
        self.virtualmachine = VirtualMachine(opennebula_id=self.opennebula_id,
                                             template=self.template)
        
    def test_model_can_create_a_virtualmachine(self):
        """Test the virtualmachine model can create a virtualmachine."""
        old_count = VirtualMachine.objects.count()
        self.virtualmachine.save()
        new_count = VirtualMachine.objects.count()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_delete_a_virtualmachine(self):
        """Test the virtualmachine model can delete a virtualmachine."""
        self.virtualmachine.save()
        old_count = VirtualMachine.objects.count()
        VirtualMachine.objects.first().delete()
        new_count = VirtualMachine.objects.count()
        self.assertNotEqual(old_count, new_count)

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
        try:
            user_pool = self.manager._get_user_pool()
        except:
            user_pool = None
        self.assertFalse(user_pool is None)

    def test_model_can_create_user(self):
        """Test the opennebula manager model can create a new user."""
        old_count = len(self.manager._get_user_pool())
        self.manager = OpenNebulaManager(email=self.email,
                                         password=self.password,
                                         create_user=True)
        user_pool = self.manager._get_user_pool()
        new_count = len(user_pool)
        # Remove the user afterwards
        user = user_pool.get_by_name(self.email)
        user.delete()
        
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
        self.opennebula_id = self.manager.create_template(name=self.template_name,
                                                          cores=self.cores,
                                                          memory=self.memory,
                                                          disk_size=self.disk_size)

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
        # Remove the template afterwards
        template = self.manager._get_template(self.template.opennebula_id)
        template.delete()
        self.assertNotEqual(old_count, new_count)

    def test_model_can_calculate_price(self):
        price = self.cores * self.core_price
        price += self.memory * self.memory_price
        price += self.disk_size * self.disk_size_price 
        self.assertEqual(price, self.template.calculate_price())



class VirtualMachineTestCase(TestCase):
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
        self.opennebula_id = self.manager.create_template(name=self.template_name,
                                                          cores=self.cores,
                                                          memory=self.memory,
                                                          disk_size=self.disk_size)

        self.template = VirtualMachineTemplate(opennebula_id=self.opennebula_id,
                                               base_price=self.base_price,
                                               memory_price=self.memory_price,
                                               core_price=self.core_price,
                                               disk_size_price=self.disk_size_price)
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

    def test_model_can_create_a_virtualmachine_for_user(self):
        pass

    def test_model_can_delete_a_virtualmachine(self):
        """Test the virtualmachine model can delete a virtualmachine."""
        self.virtualmachine.save()
        old_count = VirtualMachine.objects.count()
        VirtualMachine.objects.first().delete()
        new_count = VirtualMachine.objects.count()
        self.assertNotEqual(old_count, new_count)

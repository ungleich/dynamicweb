from django.test import TestCase
from .models import HostingPlan, HostingOrder, UserHostingKey, HostingBill
from model_mommy import mommy
from membership.models import StripeCustomer
from utils.models import BillingAddress


class VirtualMachineTypeModelTest(TestCase):

    def setUp(self):
        self.HETZNER_NUG_NAME = 'hetzner_nug'
        self.HETZNER_NAME = 'hetzner'
        self.HETZNER_RAID6_NAME = 'hetzner_raid6'
        self.HETZNER_GLUSTERFS_NAME = 'hetzner_glusterfs'
        self.BERN_NAME = 'bern'
        self.HETZNER_NUG_EXPECTED_PRICE = 79
        self.HETZNER_EXPECTED_PRICE = 180
        self.HETZNER_RAID6_EXPECTED_PRICE = 216
        self.HETZNER_GLUSTERFS_EXPECTED_PRICE = 252
        self.BERN_EXPECTED_PRICE = 202


class HostingPlanTest(TestCase):

    def serialize_test(self):
        self.hosting_plan = mommy.make(HostingPlan)
        response = {
            'id': self.hosting_plan.id,
            'cpu': self.hosting_plan.cpu_cores,
            'memory': self.hosting_plan.memory,
            'disk_size': self.hosting_plan.disk_size,
            'price': self.hosting_plan.price(),
        }
        self.assertEqual(self.hosting_plan.serialize(), response)
        self.assertEqual(self.hosting_plan.get_serialized_configs(), [response])


class HostingOrderTest(TestCase):

    def setUp(self):
        self.hosting_order = mommy.make(HostingOrder)

    def str_test(self):
        self.assertEqual(str(self.hosting_order), str(self.hosting_order.id))

    def test_status(self):
        self.assertEqual(self.hosting_order.status, HostingOrder.ORDER_DECLINED_STATUS)

    def test_create(self):
        new_hosting_order = self.hosting_order.create(
            price=1,
            vm_id=1,
            customer=mommy.make(StripeCustomer),
            billing_address=mommy.make(BillingAddress)
        )
        self.assertIsInstance(new_hosting_order, HostingOrder)

    def test_set_approved(self):
        self.assertFalse(self.hosting_order.approved)
        self.hosting_order.set_approved()
        self.assertTrue(self.hosting_order.approved)

    def test_set_stripe_charge(self):

        class TestSource(object):
            def __init__(self, last4, brand):
                self.last4 = last4
                self.brand = brand


        class TestStripe(object):

            def __init__(self, id, source):
                self.id = id
                self.source = source

        test_last4 = '1234'
        test_brand = 'VISA'

        test_stripe = TestStripe(id=1, source=TestSource(last4=test_last4, brand=test_brand))
        self.hosting_order.set_stripe_charge(stripe_charge=test_stripe)
        response = {
            'last4': test_last4,
            'cc_brand': test_brand
        }
        self.assertEqual(self.hosting_order.get_cc_data(), response)

class UserHostingKeyTest(TestCase):

    def setUp(self):
        self.hosting_order_key = mommy.make(UserHostingKey)

    def test_generate_RSA(self):
        private_key, public_key = self.hosting_order_key.generate_keys()
        self.assertTrue(len(private_key))
        self.assertTrue(len(public_key))


class HostingBillTest(TestCase):

    def setUp(self):
        self.hosting_bill = mommy.make(HostingBill)

    def test_str(self):
        self.assertEqual(str(self.hosting_bill), self.hosting_bill.customer.user.email)

    def test_create(self):
        new_hosting_order = self.hosting_bill.create(
            customer=mommy.make(StripeCustomer),
            billing_address=mommy.make(BillingAddress)
        )
        self.assertIsInstance(new_hosting_order, HostingBill)

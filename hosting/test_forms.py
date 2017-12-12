from django.test import TestCase
from model_mommy import mommy
from .forms import HostingUserLoginForm, HostingUserSignupForm


class HostingUserLoginFormTest(TestCase):
    def setUp(self):
        password = 'user_password'
        self.user = mommy.make('CustomUser', validated=1)
        self.user.set_password(password)
        self.user.save()
        self.completed_data = {
            'email': self.user.email,
            'password': password
        }
        self.incorrect_data = {
            'email': 'test',
        }

    def test_valid_form(self):
        form = HostingUserLoginForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = HostingUserLoginForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())


class HostingUserSignupFormTest(TestCase):
    def setUp(self):
        self.completed_data = {
            'name': 'test name',
            'email': 'test@ungleich.com',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }

        self.incorrect_data = {
            'email': 'test',
        }

    def test_valid_form(self):
        form = HostingUserSignupForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = HostingUserSignupForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())


class HostingOrderAdminFormTest(TestCase):
    def setUp(self):
        self.customer = mommy.make('StripeCustomer')
        self.vm_plan = mommy.make('VirtualMachinePlan')
        # self.vm_canceled_plan = mommy.make('VirtualMachinePlan',
        #                                   status=VirtualMachinePlan.CANCELED_STATUS)

        self.mocked_charge = {
            'amount': 5100,
            'amount_refunded': 0,
            'balance_transaction': 'txn_18U99zGjsLAXdRPzUJKkBx3Q',
            'captured': True,
            'created': 1467785123,
            'currency': 'chf',
            'customer': 'cus_8V61MvJvMd0PhM',
            'status': 'succeeded'
        }

        self.completed_data = {
            'customer': self.customer.id,
            'vm_plan': self.vm_plan.id,
        }

        self.incompleted_data = {
            'vm_plan': self.vm_plan.id,
            'customer': None
        }

        # @mock.patch('utils.stripe_utils.StripeUtils.make_charge')
        # def test_valid_form(self, stripe_mocked_call):
        #     stripe_mocked_call.return_value = {
        #         'paid': True,
        #         'response_object': self.mocked_charge,
        #         'error': None
        #     }
        #     form = HostingOrderAdminForm(data=self.completed_data)
        #     self.assertTrue(form.is_valid())

        # @mock.patch('utils.stripe_utils.StripeUtils.make_charge')
        # def test_invalid_form_canceled_vm(self, stripe_mocked_call):
        #
        #     self.completed_data.update({
        #         'vm_plan': self.vm_canceled_plan.id
        #     })
        #     stripe_mocked_call.return_value = {
        #         'paid': True,
        #         'response_object': self.mocked_charge,
        #         'error': None
        #     }
        #     form = HostingOrderAdminForm(data=self.completed_data)
        #     self.assertFalse(form.is_valid())
        #
        # def test_invalid_form(self):
        #     form = HostingOrderAdminForm(data=self.incompleted_data)
        #     self.assertFalse(form.is_valid())

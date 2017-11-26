import uuid
from time import sleep
from unittest.mock import patch

import stripe
from celery.result import AsyncResult
from django.conf import settings
from django.http.request import HttpRequest
from django.test import Client
from django.test import TestCase, override_settings
from unittest import skipIf
from model_mommy import mommy

from datacenterlight.models import StripePlan
from membership.models import StripeCustomer
from utils.stripe_utils import StripeUtils
from .tasks import save_ssh_key


class BaseTestCase(TestCase):
    """
    Base class to initialize the test cases
    """

    def setUp(self):
        # Password
        self.dummy_password = 'test_password'

        # Users
        self.customer, self.another_customer = mommy.make(
            'membership.CustomUser', validated=1, _quantity=2
        )
        self.customer.set_password(self.dummy_password)
        self.customer.save()
        self.another_customer.set_password(self.dummy_password)
        self.another_customer.save()

        # Stripe mocked data
        self.stripe_mocked_customer = self.customer_stripe_mocked_data()

        #  Clients
        self.customer_client = self.get_client(self.customer)
        self.another_customer_client = self.get_client(self.another_customer)

        # Request Object
        self.request = HttpRequest()
        self.request.META['SERVER_NAME'] = 'ungleich.com'
        self.request.META['SERVER_PORT'] = '80'

    def get_client(self, user):
        """
        Authenticate a user and return the client
        """
        client = Client()
        client.login(email=user.email, password=self.dummy_password)
        return client

    def customer_stripe_mocked_data(self):
        return {
            "id": "cus_8R1y9UWaIIjZqr",
            "object": "customer",
            "currency": "usd",
            "default_source": "card_18A9up2eZvKYlo2Cq2RJMGeF",
            "email": "vmedixtodd+1@gmail.com",
            "livemode": False,
            "metadata": {
            },
            "shipping": None,
            "sources": {
                "object": "list",
                "data": [{
                    "id": "card_18A9up2eZvKYlo2Cq2RJMGeF",
                    "object": "card",
                    "brand": "Visa",
                    "country": "US",
                    "customer": "cus_8R1y9UWaIIjZqr",
                    "cvc_check": "pass",
                    "dynamic_last4": None,
                    "exp_month": 12,
                    "exp_year": 2018,
                    "funding": "credit",
                    "last4": "4242",
                }]
            }
        }

    def setup_view(self, view, *args, **kwargs):
        """Mimic as_view() returned callable, but returns view instance.

        args and kwargs are the same you would pass to ``reverse()``

        """
        view.request = self.request
        view.args = args
        view.kwargs = kwargs
        view.config = None
        return view


@skipIf(settings.STRIPE_API_PRIVATE_KEY_TEST is None or
        settings.STRIPE_API_PRIVATE_KEY_TEST is "",
        """Skip because STRIPE_API_PRIVATE_KEY_TEST is not set""")
class TestStripeCustomerDescription(TestCase):
    """
    A class to test setting the description field of the stripe customer
    https://stripe.com/docs/api#metadata
    """

    def setUp(self):
        self.customer_password = 'test_password'
        self.customer_email = 'test@ungleich.ch'
        self.customer_name = "Monty Python"
        self.customer = mommy.make('membership.CustomUser')
        self.customer.set_password(self.customer_password)
        self.customer.email = self.customer_email
        self.customer.save()
        self.stripe_utils = StripeUtils()
        stripe.api_key = settings.STRIPE_API_PRIVATE_KEY_TEST
        self.token = stripe.Token.create(
            card={
                "number": '4111111111111111',
                "exp_month": 12,
                "exp_year": 2022,
                "cvc": '123'
            },
        )
        self.failed_token = stripe.Token.create(
            card={
                "number": '4000000000000341',
                "exp_month": 12,
                "exp_year": 2022,
                "cvc": '123'
            },
        )

    def test_creating_stripe_customer(self):
        stripe_data = self.stripe_utils.create_customer(self.token.id,
                                                        self.customer.email,
                                                        self.customer_name)
        self.assertEqual(stripe_data.get('error'), None)
        customer_data = stripe_data.get('response_object')
        self.assertEqual(customer_data.description, self.customer_name)


@skipIf(settings.STRIPE_API_PRIVATE_KEY_TEST == "" or
        settings.TEST_MANAGE_SSH_KEY_HOST == "",
        """Skipping test_save_ssh_key_add because either host
         or public key were not specified or were empty""")
class StripePlanTestCase(TestStripeCustomerDescription):
    """
    A class to test Stripe plans
    """

    def test_get_stripe_plan_id_string(self):
        plan_id_string = StripeUtils.get_stripe_plan_id(cpu=2, ram=20, ssd=100,
                                                        version=1, app='dcl')
        self.assertEqual(plan_id_string, 'dcl-v1-cpu-2-ram-20gb-ssd-100gb')
        plan_id_string = StripeUtils.get_stripe_plan_id(cpu=2, ram=20, ssd=100,
                                                        version=1, app='dcl',
                                                        hdd=200)
        self.assertEqual(plan_id_string,
                         'dcl-v1-cpu-2-ram-20gb-ssd-100gb-hdd-200gb')

    def test_get_or_create_plan(self):
        stripe_plan = self.stripe_utils.get_or_create_stripe_plan(2000,
                                                                  "test plan 1",
                                                                  stripe_plan_id='test-plan-1')
        self.assertIsNone(stripe_plan.get('error'))
        self.assertIsInstance(stripe_plan.get('response_object'), StripePlan)

    @skipIf(settings.TEST_MANAGE_SSH_KEY_PUBKEY == "" or
            settings.TEST_MANAGE_SSH_KEY_HOST == "",
            """Skipping test_save_ssh_key_add because either host
             or public key were not specified or were empty""")
    @patch('utils.stripe_utils.logger')
    def test_create_duplicate_plans_error_handling(self, mock_logger):
        """
        Test details:
            1. Create a test plan in Stripe with a particular id
            2. Try to recreate the plan with the same id
            3. This creates a Stripe error, the code should be able to handle the error

        :param mock_logger:
        :return:
        """
        unique_id = str(uuid.uuid4().hex)
        new_plan_id_str = 'test-plan-{}'.format(unique_id)
        stripe_plan = self.stripe_utils.get_or_create_stripe_plan(2000,
                                                                  "test plan {}".format(
                                                                      unique_id),
                                                                  stripe_plan_id=new_plan_id_str)
        self.assertIsInstance(stripe_plan.get('response_object'), StripePlan)
        self.assertEqual(stripe_plan.get('response_object').stripe_plan_id,
                         new_plan_id_str)

        # Test creating the same plan again and expect the PLAN_EXISTS_ERROR_MSG
        # We first delete the local Stripe Plan, so that the code tries to create a new plan in Stripe
        StripePlan.objects.filter(
            stripe_plan_id=new_plan_id_str).all().delete()
        stripe_plan_1 = self.stripe_utils.get_or_create_stripe_plan(2000,
                                                                    "test plan {}".format(
                                                                        unique_id),
                                                                    stripe_plan_id=new_plan_id_str)
        mock_logger.debug.assert_called_with(
            self.stripe_utils.PLAN_EXISTS_ERROR_MSG.format(new_plan_id_str))
        self.assertIsInstance(stripe_plan_1.get('response_object'), StripePlan)
        self.assertEqual(stripe_plan_1.get('response_object').stripe_plan_id,
                         new_plan_id_str)

        # Delete the test stripe plan that we just created
        delete_result = self.stripe_utils.delete_stripe_plan(new_plan_id_str)
        self.assertIsInstance(delete_result, dict)
        self.assertEqual(delete_result.get('response_object'), True)

    @patch('utils.stripe_utils.logger')
    def test_delete_unexisting_plan_should_fail(self, mock_logger):
        plan_id = 'crazy-plan-id-that-does-not-exist'
        result = self.stripe_utils.delete_stripe_plan(plan_id)
        self.assertIsInstance(result, dict)
        self.assertEqual(result.get('response_object'), False)
        mock_logger.debug.assert_called_with(
            self.stripe_utils.PLAN_DOES_NOT_EXIST_ERROR_MSG.format(plan_id))

    def test_subscribe_customer_to_plan(self):
        stripe_plan = self.stripe_utils.get_or_create_stripe_plan(2000,
                                                                  "test plan 1",
                                                                  stripe_plan_id='test-plan-1')
        stripe_customer = StripeCustomer.get_or_create(
            email=self.customer_email,
            token=self.token)
        result = self.stripe_utils.subscribe_customer_to_plan(
            stripe_customer.stripe_id,
            [{"plan": stripe_plan.get(
                'response_object').stripe_plan_id}])
        self.assertIsInstance(result.get('response_object'),
                              stripe.Subscription)
        self.assertIsNone(result.get('error'))
        self.assertEqual(result.get('response_object').get('status'), 'active')

    def test_subscribe_customer_to_plan_failed_payment(self):
        stripe_plan = self.stripe_utils.get_or_create_stripe_plan(2000,
                                                                  "test plan 1",
                                                                  stripe_plan_id='test-plan-1')
        stripe_customer = StripeCustomer.get_or_create(
            email=self.customer_email,
            token=self.failed_token)
        result = self.stripe_utils.subscribe_customer_to_plan(
            stripe_customer.stripe_id,
            [{"plan": stripe_plan.get(
                'response_object').stripe_plan_id}])
        self.assertIsNone(result.get('response_object'), None)
        self.assertIsNotNone(result.get('error'))


class SaveSSHKeyTestCase(TestCase):
    """
    A test case to test the celery save_ssh_key task
    """

    @override_settings(
        task_eager_propagates=True,
        task_always_eager=True,
    )
    def setUp(self):
        self.public_key = settings.TEST_MANAGE_SSH_KEY_PUBKEY
        self.hosts = settings.TEST_MANAGE_SSH_KEY_HOST

    @skipIf(settings.TEST_MANAGE_SSH_KEY_PUBKEY is "" or
            settings.TEST_MANAGE_SSH_KEY_PUBKEY is None or
            settings.TEST_MANAGE_SSH_KEY_HOST is "" or
            settings.TEST_MANAGE_SSH_KEY_HOST is None,
            """Skipping test_save_ssh_key_add because either host
             or public key were not specified or were empty""")
    def test_save_ssh_key_add(self):
        async_task = save_ssh_key.delay([self.hosts],
                                        [{'value': self.public_key,
                                          'state': True}])
        save_ssh_key_result = None
        for i in range(0, 10):
            sleep(5)
            res = AsyncResult(async_task.task_id)
            if type(res.result) is bool:
                save_ssh_key_result = res.result
                break
        self.assertIsNotNone(save_ssh_key, "save_ssh_key_result is None")
        self.assertTrue(save_ssh_key_result, "save_ssh_key_result is False")

    @skipIf(settings.TEST_MANAGE_SSH_KEY_PUBKEY is None or
            settings.TEST_MANAGE_SSH_KEY_PUBKEY == "" or
            settings.TEST_MANAGE_SSH_KEY_HOST is None or
            settings.TEST_MANAGE_SSH_KEY_HOST is "",
            """Skipping test_save_ssh_key_add because either host
             or public key were not specified or were empty""")
    def test_save_ssh_key_remove(self):
        async_task = save_ssh_key.delay([self.hosts],
                                        [{'value': self.public_key,
                                          'state': False}])
        save_ssh_key_result = None
        for i in range(0, 10):
            sleep(5)
            res = AsyncResult(async_task.task_id)
            if type(res.result) is bool:
                save_ssh_key_result = res.result
                break
        self.assertIsNotNone(save_ssh_key, "save_ssh_key_result is None")
        self.assertTrue(save_ssh_key_result, "save_ssh_key_result is False")

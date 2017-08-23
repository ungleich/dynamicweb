# from django.test import TestCase

from time import sleep

import stripe
from celery.result import AsyncResult
from django.conf import settings
from django.core.management import call_command
# Create your tests here.
from django.test import TestCase, override_settings
from model_mommy import mommy

from datacenterlight.models import VMTemplate
from datacenterlight.tasks import create_vm_task
from membership.models import StripeCustomer
from opennebula_api.serializers import VMTemplateSerializer
from utils.models import BillingAddress
from utils.stripe_utils import StripeUtils


class CeleryTaskTestCase(TestCase):
    @override_settings(
        task_eager_propagates=True,
        task_always_eager=True,
    )
    def setUp(self):
        self.customer_password = 'test_password'
        self.customer_email = 'celery-createvm-task-test@ungleich.ch'
        self.customer_name = "Monty Python"
        self.user = {
            'email': self.customer_email,
            'name': self.customer_name
        }
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
        # Run fetchvmtemplates so that we have the VM templates from
        # OpenNebula
        call_command('fetchvmtemplates')

    def test_create_vm_task(self):
        """Tests the create vm task."""

        # We create a VM from the first template available to DCL
        vm_template = VMTemplate.objects.all().first()
        template_data = VMTemplateSerializer(vm_template).data

        # The specs of VM that we want to create
        specs = {
            'cpu': 1,
            'memory': 2,
            'disk_size': 10,
            'price': 15,
        }

        stripe_customer = StripeCustomer.get_or_create(
            email=self.customer_email,
            token=self.token)
        billing_address = BillingAddress(
            cardholder_name=self.customer_name,
            postal_code='1232',
            country='CH',
            street_address='Monty\'s Street',
            city='Hollywood')
        billing_address.save()
        billing_address_data = {'cardholder_name': self.customer_name,
                                'postal_code': '1231',
                                'country': 'CH',
                                'token': self.token,
                                'street_address': 'Monty\'s Street',
                                'city': 'Hollywood'}

        billing_address_id = billing_address.id
        vm_template_id = template_data.get('id', 1)
        final_price = specs.get('price')

        # Make stripe charge to a customer
        stripe_utils = StripeUtils()
        charge_response = stripe_utils.make_charge(
            amount=final_price,
            customer=stripe_customer.stripe_id)

        # Check if the payment was approved
        if not charge_response.get(
                'response_object'):
            msg = charge_response.get('error')
            raise Exception("make_charge failed: {}".format(msg))

        charge = charge_response.get('response_object')
        async_task = create_vm_task.delay(vm_template_id, self.user,
                                          specs,
                                          template_data,
                                          stripe_customer.id,
                                          billing_address_data,
                                          billing_address_id,
                                          charge)
        new_vm_id = 0
        res = None
        for i in range(0, 10):
            sleep(5)
            res = AsyncResult(async_task.task_id)
            if res.result is not None and res.result > 0:
                new_vm_id = res.result
                break

        # We expect a VM to be created within 50 seconds
        self.assertGreater(new_vm_id, 0,
                           "VM could not be created. res._get_task_meta() = {}"
                           .format(res._get_task_meta()))

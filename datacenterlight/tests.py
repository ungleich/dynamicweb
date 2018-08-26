# from django.test import TestCase

from time import sleep

import stripe
from celery.result import AsyncResult
from django.conf import settings
from django.core.management import call_command
from django.test import TestCase, override_settings
from model_mommy import mommy
from unittest import skipIf

from datacenterlight.models import VMTemplate
from datacenterlight.tasks import create_vm_task
from hosting.models import HostingOrder
from membership.models import StripeCustomer
from opennebula_api.serializers import VMTemplateSerializer
from utils.hosting_utils import get_vm_price
from utils.models import BillingAddress
from utils.stripe_utils import StripeUtils


@skipIf(
        settings.STRIPE_API_PRIVATE_KEY_TEST is None or
        settings.STRIPE_API_PRIVATE_KEY_TEST is "",
        """Stripe details unavailable, so skipping CeleryTaskTestCase"""
    )
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

    @skipIf(
        settings.OPENNEBULA_DOMAIN is None or settings.OPENNEBULA_DOMAIN is
        "test_domain",
        """OpenNebula details unavailable, so skipping test_create_vm_task"""
    )
    def test_create_vm_task(self):
        """Tests the create vm task for monthly subscription

        This test is supposed to validate the proper execution
        of celery create_vm_task on production, as we have no
        other way to do this.
        """

        # We create a VM from the first template available to DCL
        vm_template = VMTemplate.objects.all().first()
        template_data = VMTemplateSerializer(vm_template).data

        # The specs of VM that we want to create
        specs = {
            'cpu': 1,
            'memory': 2,
            'disk_size': 10,
            'price': 15
        }

        stripe_customer = StripeCustomer.get_or_create(
            email=self.customer_email,
            token=self.token
        )
        card_details = self.stripe_utils.get_card_details(
            stripe_customer.stripe_id
        )
        card_details_dict = card_details.get('error')
        self.assertEquals(card_details_dict, None)
        billing_address_data = {'cardholder_name': self.customer_name,
                                'postal_code': '1231',
                                'country': 'CH',
                                'token': self.token,
                                'street_address': 'Monty\'s Street',
                                'city': 'Hollywood'}
        vm_template_id = template_data.get('id', 1)

        cpu = specs.get('cpu')
        memory = specs.get('memory')
        disk_size = specs.get('disk_size')
        amount_to_be_charged = get_vm_price(cpu=cpu, memory=memory,
                                            disk_size=disk_size)
        plan_name = StripeUtils.get_stripe_plan_name(cpu=cpu,
                                                     memory=memory,
                                                     disk_size=disk_size)
        stripe_plan_id = StripeUtils.get_stripe_plan_id(cpu=cpu,
                                                        ram=memory,
                                                        ssd=disk_size,
                                                        version=1,
                                                        app='dcl')
        stripe_plan = self.stripe_utils.get_or_create_stripe_plan(
            amount=amount_to_be_charged,
            name=plan_name,
            stripe_plan_id=stripe_plan_id)
        subscription_result = self.stripe_utils.subscribe_customer_to_plan(
            stripe_customer.stripe_id,
            [{"plan": stripe_plan.get(
                'response_object').stripe_plan_id}])
        stripe_subscription_obj = subscription_result.get('response_object')
        # Check if the subscription was approved and is active
        if stripe_subscription_obj is None \
                or stripe_subscription_obj.status != 'active':
            msg = subscription_result.get('error')
            raise Exception("Creating subscription failed: {}".format(msg))

        billing_address = BillingAddress(
            cardholder_name=billing_address_data['cardholder_name'],
            street_address=billing_address_data['street_address'],
            city=billing_address_data['city'],
            postal_code=billing_address_data['postal_code'],
            country=billing_address_data['country']
        )
        billing_address.save()

        order = HostingOrder.create(
            price=specs['price'],
            vm_id=0,
            customer=stripe_customer,
            billing_address=billing_address
        )

        async_task = create_vm_task.delay(
            vm_template_id, self.user, specs, template_data, order.id
        )
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

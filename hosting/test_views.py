from django.conf import settings
from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from unittest import skipIf

from model_mommy import mommy
from stored_messages.models import Inbox


from membership.models import CustomUser, StripeCustomer
from .models import HostingOrder
from .views import (
    DjangoHostingView, RailsHostingView, NodeJSHostingView, LoginView,
    SignupView, PaymentVMView, OrdersHostingDetailView, OrdersHostingListView,
    VirtualMachinesPlanListView, PasswordResetView, PasswordResetConfirmView,
    HostingPricingView, NotificationsView, MarkAsReadNotificationView
)
from utils.tests import BaseTestCase


@skipIf(
    (settings.OPENNEBULA_DOMAIN is None or
     settings.OPENNEBULA_DOMAIN == "test_domain"),
    """OpenNebula details unavailable, so skipping
     ProcessVMSelectionTestMixin"""
)
class ProcessVMSelectionTestMixin(object):

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.view.get_context_data(), self.expected_context)
        self.assertEqual(response.context['hosting'], self.expected_context['hosting'])
        self.assertTemplateUsed(response, self.expected_template)

    # def test_anonymous_post(self):
    #     params = {'vm_template_id': 1, 'configuration': 1}
    #     response = self.client.post(self.url, params)
    #     self.assertRedirects(response, expected_url=reverse('hosting:login'),
    #                          status_code=302, target_status_code=200)


class DjangoHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('django.hosting')
        self.view = DjangoHostingView()
        self.expected_template = 'hosting/django.html'
        HOSTING = 'django'
        # configuration_detail = dict(
        # VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        self.expected_context = {
            'hosting': HOSTING,
            'hosting_long': "Django",
            # 'configuration_detail': configuration_detail,
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'email': "info@django-hosting.ch",
            # 'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class RailsHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('rails.hosting')
        self.view = RailsHostingView()
        self.expected_template = 'hosting/rails.html'
        HOSTING = 'rails'
        # configuration_detail = dict(
        # VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        self.expected_context = {
            'hosting': HOSTING,
            'hosting_long': "Ruby On Rails",
            # 'configuration_detail': configuration_detail,
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            # 'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class NodeJSHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('node.hosting')
        self.view = NodeJSHostingView()
        self.expected_template = 'hosting/nodejs.html'
        HOSTING = 'nodejs'
        # configuration_detail = dict(
        # VirtualMachinePlan.VM_CONFIGURATION).get(HOSTING)
        self.expected_context = {
            'hosting': HOSTING,
            'hosting_long': "NodeJS",
            # 'configuration_detail': configuration_detail,
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            # 'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


@skipIf(
    (settings.OPENNEBULA_DOMAIN is None or
     settings.OPENNEBULA_DOMAIN == "test_domain"),
    """OpenNebula details unavailable, so skipping
     HostingPricingViewTest.test_get"""
)
class HostingPricingViewTest(TestCase):

    def setUp(self):
        self.url = reverse('hosting:pricing')
        self.view = HostingPricingView()
        self.expected_template = 'hosting/hosting_pricing.html'

        # configuration_options = dict(VirtualMachinePlan.VM_CONFIGURATION)
        self.expected_context = {
            # 'configuration_options': configuration_options,
            'email': "info@django-hosting.ch",
            # 'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(self.view.get_context_data(), self.expected_context)
        self.assertTemplateUsed(response, self.expected_template)

    # def test_anonymous_post(self):
    #     response = self.client.post(self.url)
    #     self.assertRedirects(response, expected_url=reverse('hosting:login'),
    #                          status_code=302, target_status_code=200)


class PaymentVMViewTest(BaseTestCase):

    def setUp(self):
        super(PaymentVMViewTest, self).setUp()

        self.view = PaymentVMView

        # VM
        # self.vm = mommy.make(VirtualMachineType, base_price=10000,
        #                      memory_price=100,
        #                      core_price=1000,
        #                      disk_size_price=1)

        # post data
        self.billing_address = {
            'street_address': 'street name',
            'city': 'MyCity',
            'postal_code': '32123123123123',
            'country': 'VE',
            'token': 'a23kfmslwxhkwis'
        }

        # urls
        self.url = reverse('hosting:payment')

        # Session data
        # self.session_data = {
        #     'vm_specs': {
        #         'hosting_company': self.vm.hosting_company,
        #         'cores': 1,
        #         'memory': 10,
        #         'disk_size': 10000,
        #         'price': 22000,
        #         'configuration': dict(VirtualMachinePlan.VM_CONFIGURATION).get('django')
        #     }
        # }

        # session = self.customer_client.session
        # session.update(self.session_data)
        # session.save()

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    # @mock.patch('utils.stripe_utils.StripeUtils.create_customer')
    # def test_post(self, stripe_mocked_call):
    #
    #     # Anonymous user should get redirect to login
    #     response = self.client.post(self.url)
    #     expected_url = "%s?next=%s" % (reverse('hosting:login'), reverse('hosting:payment'))
    #     self.assertRedirects(response, expected_url=expected_url,
    #                          status_code=302, target_status_code=200)
    #
    #     # Customer user should be able to pay
    #     stripe_mocked_call.return_value = {
    #         'paid': True,
    #         'response_object': self.stripe_mocked_customer,
    #         'error': None
    #     }
    #     response = self.customer_client.post(self.url, self.billing_address)
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(StripeCustomer.objects.filter(user__email=self.customer.email).exists())
    #     stripe_customer = StripeCustomer.objects.get(user__email=self.customer.email)
    #     self.assertEqual(stripe_customer.user, self.customer)
    #     self.assertTrue(HostingOrder.objects.filter(customer=stripe_customer).exists())
    #     hosting_order = HostingOrder.objects.filter(customer=stripe_customer)[0]
    #     vm_plan = {
    #         'cores': hosting_order.vm_plan.cores,
    #         'memory': hosting_order.vm_plan.memory,
    #         'disk_size': hosting_order.vm_plan.disk_size,
    #         'price': hosting_order.vm_plan.price,
    #         'hosting_company': hosting_order.vm_plan.vm_type.hosting_company,
    #         'configuration': hosting_order.vm_plan.configuration
    #     }
    #     self.assertEqual(vm_plan, self.session_data.get('vm_specs'))

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'), reverse('hosting:payment'))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Logged user should get the page
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['stripe_key'],
                         settings.STRIPE_API_PUBLIC_KEY)


class NotificationsViewTest(BaseTestCase):

    def setUp(self):
        super(NotificationsViewTest, self).setUp()

        self.view = NotificationsView
        self.url = reverse('hosting:notifications')
        self.expected_template = 'hosting/notifications.html'

        self.inboxes = mommy.make(Inbox, user=self.customer, _quantity=2)
        self.messages = list(map(lambda x: x.message, self.inboxes))

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'), reverse('hosting:notifications'))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Logged user should get the page
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['all_notifications'], self.messages)
        self.assertTemplateUsed(response, self.expected_template)


class MarkAsReadNotificationViewTest(BaseTestCase):

    def setUp(self):
        super(MarkAsReadNotificationViewTest, self).setUp()

        self.view = MarkAsReadNotificationView
        self.url = reverse('hosting:notifications')
        self.expected_template = 'hosting/notifications.html'

        self.inbox = mommy.make(Inbox, user=self.customer)
        self.message = self.inbox.message

        self.url = reverse('hosting:read_notification', kwargs={'pk': self.message.id})

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_post(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'),
                                       reverse('hosting:read_notification',
                                               kwargs={'pk': self.message.id}))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Logged user should mark a message as read
        response = self.customer_client.post(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Inbox.objects.filter(user=self.customer).exists())
        self.assertTemplateUsed(response, self.expected_template)


# class GenerateVMSSHKeysViewTest(BaseTestCase):
#
#     def setUp(self):
#         super(GenerateVMSSHKeysViewTest, self).setUp()
#
#         # self.view = GenerateVMSSHKeysView
#         # self.vm = mommy.make(VirtualMachinePlan)
#         self.expected_template = 'hosting/virtual_machine_key.html'
#         self.url = reverse('hosting:virtual_machine_key', kwargs={'pk': self.vm.id})
#
#     def test_url_resolve_to_view_correctly(self):
#         found = resolve(self.url)
#         self.assertEqual(found.func.__name__, self.view.__name__)
#
#     def test_get(self):
#
#         # Anonymous user should get redirect to login
#         response = self.client.get(self.url)
#         expected_url = "%s?next=%s" % (reverse('hosting:login'),
#                                        reverse('hosting:virtual_machine_key',
#                                                kwargs={'pk': self.vm.id}))
#         self.assertRedirects(response, expected_url=expected_url,
#                              status_code=302, target_status_code=200)
#
#         # Logged user should get the page
#         response = self.customer_client.get(self.url, follow=True)
#         self.assertEqual(response.status_code, 200)
#         #updated_vm = VirtualMachinePlan.objects.get(id=self.vm.id)
#         #self.assertEqual(response.context['public_key'].decode("utf-8"), updated_vm.public_key)
#         self.assertTrue(response.context['private_key'] is not None)
#         self.assertEqual(len(response.context['public_key']), 380)
#         self.assertTrue(len(response.context['private_key']) is 1678 or 1674)
#         self.assertTemplateUsed(response, self.expected_template)


# class VirtualMachineViewTest(BaseTestCase):
#
#     def setUp(self):
#         super(VirtualMachineViewTest, self).setUp()
#
#         self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
#         #self.vm = mommy.make(VirtualMachinePlan)
#         self.vm.assign_permissions(self.customer)
#         self.order = mommy.make(HostingOrder, customer=self.stripe_customer, vm_plan=self.vm)
#         self.url = reverse('hosting:virtual_machines', kwargs={'pk': self.vm.id})
#         self.view = VirtualMachineView()
#         self.expected_template = 'hosting/virtual_machine_detail.html'
#
#     def url_resolve_to_view_correctly(self):
#         found = resolve(self.url)
#         self.assertEqual(found.func.__name__, self.view.__name__)
#
#     def test_get(self):
#
#         # Anonymous user should get redirect to login
#         response = self.client.get(self.url)
#         expected_url = "%s?next=%s" % (reverse('hosting:login'),
#                                        reverse('hosting:virtual_machines',
#                                        kwargs={'pk': self.vm.id}))
#         self.assertRedirects(response, expected_url=expected_url,
#                              status_code=302, target_status_code=200)
#
#         # Customer should be able to get data
#         response = self.customer_client.get(self.url, follow=True)
#         self.assertEqual(response.status_code, 200)
#         self.assertEqual(response.context['virtual_machine'], self.vm)
#         self.assertTemplateUsed(response, self.expected_template)


class VirtualMachinesPlanListViewTest(BaseTestCase):

    def setUp(self):
        super(VirtualMachinesPlanListViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        mommy.make(HostingOrder, customer=self.stripe_customer, approved=True, _quantity=20)
        # _vms = VirtualMachinePlan.objects.all()
        # self.vms = sorted(_vms, key=lambda vm: vm.id, reverse=True)
        self.url = reverse('hosting:virtual_machines')
        self.view = VirtualMachinesPlanListView()
        self.expected_template = 'hosting/virtual_machines.html'

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'),
                                       reverse('hosting:virtual_machines'))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Customer should be able to get his orders
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        # self.assertEqual(list(response.context['vms']), self.vms[:10])
        self.assertTemplateUsed(response, self.expected_template)


class OrderHostingDetailViewTest(BaseTestCase):

    def setUp(self):
        super(OrderHostingDetailViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        self.order = mommy.make(HostingOrder, customer=self.stripe_customer)
        self.order.assign_permissions(self.customer)
        self.url = reverse('hosting:orders', kwargs={'pk': self.order.id})
        self.view = OrdersHostingDetailView()
        self.expected_template = 'hosting/order_detail.html'

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'),
                                       reverse('hosting:orders', kwargs={'pk': self.order.id}))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Customer should be able to get data
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['order'], self.order)
        self.assertTemplateUsed(response, self.expected_template)


class OrdersHostingListViewTest(BaseTestCase):

    def setUp(self):
        super(OrdersHostingListViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        _orders = mommy.make(HostingOrder, customer=self.stripe_customer, _quantity=20)
        self.orders = sorted(_orders, key=lambda order: order.id, reverse=True)
        self.url = reverse('hosting:orders')
        self.view = OrdersHostingListView()
        self.expected_template = 'hosting/orders.html'

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'), reverse('hosting:orders'))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Customer should be able to get his orders
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(list(response.context['orders']), self.orders[:10])
        self.assertTemplateUsed(response, self.expected_template)


class LoginViewTest(TestCase):

    def setUp(self):
        self.url = reverse('hosting:login')
        self.view = LoginView
        self.expected_template = 'hosting/login.html'
        self.user = mommy.make('membership.CustomUser', validated=1)
        self.password = 'fake_password'
        self.user.set_password(self.password)
        self.user.save()

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)

    def test_anonymous_user_can_login(self):
        data = {
            'email': self.user.email,
            'password': self.password
        }
        response = self.client.post(self.url, data=data, follow=True)
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.status_code, 200)


class SignupViewTest(TestCase):

    def setUp(self):
        self.url = reverse('hosting:signup')
        self.expected_template = 'hosting/signup.html'
        self.view = SignupView
        self.signup_data = {
            'name': 'ungleich',
            'email': 'test@ungleich.com',
            'password': 'fake_password',
            'confirm_password': 'fake_password',
        }

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)

    def test_anonymous_user_can_signup(self):
        response = self.client.post(self.url, data=self.signup_data, follow=True)
        self.user = CustomUser.objects.get(email=self.signup_data.get('email'))
        # self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.status_code, 200)


class PasswordResetViewTest(BaseTestCase):

    def setUp(self):
        super(PasswordResetViewTest, self).setUp()

        self.url = reverse('hosting:reset_password')
        self.view = PasswordResetView
        self.expected_template = 'hosting/reset_password.html'
        self.user = mommy.make('membership.CustomUser')
        self.password = 'fake_password'
        self.user.set_password(self.password)
        self.user.save()

        self.post_data = {
            'email': self.user.email
        }

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)

    def test_post(self):
        response = self.client.post(self.url, data=self.post_data, follow=True)
        self.assertEqual(response.status_code, 200)

    def test_test_generate_email_context(self):
        context = self.setup_view(self.view()).test_generate_email_context(
            self.user
        )
        self.assertEqual(context.get('user'), self.user)
        self.assertEqual(context.get('site_name'), settings.DCL_TEXT)
        self.assertEqual(len(context.get('token')), 24)


class PasswordResetConfirmViewTest(BaseTestCase):

    def setUp(self):
        super(PasswordResetConfirmViewTest, self).setUp()

        self.view = PasswordResetConfirmView
        self.expected_template = 'hosting/confirm_reset_password.html'
        self.user = mommy.make('membership.CustomUser')
        self.password = 'fake_password'
        self.user.set_password(self.password)
        self.user.save()

        self.token = default_token_generator.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.url = reverse('hosting:reset_password_confirm',
                           kwargs={'token': self.token, 'uidb64': self.uid})

        self.post_data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password'
        }

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, self.expected_template)

    # def test_post(self):
    #     response = self.client.post(
    #         self.url, data=self.post_data, follow=True
    #     )
    #     self.assertEqual(response.status_code, 200)
    #     self.assertTrue(not response.context['form'].errors)

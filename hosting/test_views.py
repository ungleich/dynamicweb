from unittest import mock
from django.conf import settings
from django.test import TestCase, RequestFactory
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve

from model_mommy import mommy


from membership.models import CustomUser, StripeCustomer
from .models import VirtualMachineType, HostingOrder, VirtualMachinePlan
from .views import DjangoHostingView, RailsHostingView, NodeJSHostingView, LoginView, SignupView, \
    PaymentVMView, OrdersHostingDetailView, OrdersHostingListView, VirtualMachineDetailView, \
    VirtualMachinesPlanListView
from utils.tests import BaseTestCase


class ProcessVMSelectionTestMixin(object):

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.view.get_context_data(), self.expected_context)
        self.assertEqual(response.context['hosting'], self.expected_context['hosting'])
        self.assertTemplateUsed(response, self.expected_template)

    def test_anonymous_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url=reverse('hosting:login'),
                             status_code=302, target_status_code=200)


class DjangoHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('django.hosting')
        self.view = DjangoHostingView()
        self.expected_template = 'hosting/django.html'
        self.expected_context = {
            'hosting': "django",
            'hosting_long': "Django",
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'email': "info@django-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class RailsHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('rails.hosting')
        self.view = RailsHostingView()
        self.expected_template = 'hosting/rails.html'
        self.expected_context = {
            'hosting': "rails",
            'hosting_long': "Ruby On Rails",
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class NodeJSHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('node.hosting')
        self.view = NodeJSHostingView()
        self.expected_template = 'hosting/nodejs.html'
        self.expected_context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class PaymentVMViewTest(BaseTestCase):

    def setUp(self):
        super(PaymentVMViewTest, self).setUp()

        self.view = PaymentVMView

        # VM
        self.vm = mommy.make(VirtualMachineType, base_price=10000,
                             memory_price=100,
                             core_price=1000,
                             disk_size_price=1)

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
        self.session_data = {
            'vm_specs': {
                'hosting_company': self.vm.hosting_company,
                'cores': 1,
                'memory': 10,
                'disk_size': 10000,
                'price': 22000,
            }
        }

        session = self.customer_client.session
        session.update(self.session_data)
        session.save()

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    @mock.patch('utils.stripe_utils.StripeUtils.create_customer')
    def test_post(self, stripe_mocked_call):

        # Anonymous user should get redirect to login
        response = self.client.post(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'), reverse('hosting:payment'))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Customer user should be able to pay
        stripe_mocked_call.return_value = {
            'paid': True,
            'response_object': self.stripe_mocked_customer,
            'error': None
        }
        response = self.customer_client.post(self.url, self.billing_address)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(StripeCustomer.objects.filter(user__email=self.customer.email).exists())
        stripe_customer = StripeCustomer.objects.get(user__email=self.customer.email)
        self.assertEqual(stripe_customer.user, self.customer)
        self.assertTrue(HostingOrder.objects.filter(customer=stripe_customer).exists())
        hosting_order = HostingOrder.objects.filter(customer=stripe_customer)[0]
        vm_plan = {
            'cores': hosting_order.vm_plan.cores,
            'memory': hosting_order.vm_plan.memory,
            'disk_size': hosting_order.vm_plan.disk_size,
            'price': hosting_order.vm_plan.price,
            'hosting_company': hosting_order.vm_plan.vm_type.hosting_company
        }
        self.assertEqual(vm_plan, self.session_data.get('vm_specs'))

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


class VirtualMachineDetailViewTest(BaseTestCase):

    def setUp(self):
        super(VirtualMachineDetailViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        self.vm = mommy.make(VirtualMachinePlan)
        self.order = mommy.make(HostingOrder, customer=self.stripe_customer, vm_plan=self.vm)
        self.url = reverse('hosting:virtual_machines', kwargs={'pk': self.vm.id})
        self.view = VirtualMachineDetailView()
        self.expected_template = 'hosting/virtual_machine_detail.html'

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (reverse('hosting:login'),
                                       reverse('hosting:virtual_machines',
                                       kwargs={'pk': self.vm.id}))
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Customer should be able to get data
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['virtual_machine'], self.vm)
        self.assertTemplateUsed(response, self.expected_template)


class VirtualMachinesPlanListViewTest(BaseTestCase):

    def setUp(self):
        super(VirtualMachinesPlanListViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        mommy.make(HostingOrder, customer=self.stripe_customer, approved=True, _quantity=20)
        _vms = VirtualMachinePlan.objects.all()
        self.vms = sorted(_vms, key=lambda vm: vm.id, reverse=True)
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
        self.assertEqual(list(response.context['vms']), self.vms[:10])
        self.assertTemplateUsed(response, self.expected_template)


class OrderHostingDetailViewTest(BaseTestCase):

    def setUp(self):
        super(OrderHostingDetailViewTest, self).setUp()

        self.stripe_customer = mommy.make(StripeCustomer, user=self.customer)
        self.order = mommy.make(HostingOrder, customer=self.stripe_customer)
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
        self.user = mommy.make('membership.CustomUser')
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
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.status_code, 200)

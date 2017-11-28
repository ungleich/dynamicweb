from model_mommy import mommy
from unittest import mock

from django.test import TestCase
from django.conf import settings
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from cms.test_utils.testcases import CMSTestCase
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from cms.api import create_page

from membership.models import CustomUser, StripeCustomer
from utils.tests import BaseTestCase


from .views import (
    LoginView, SignupView, PasswordResetView, PasswordResetConfirmView,
    MembershipPricingView, MembershipPaymentView
)
from .models import MembershipType


class ContactViewTest(TestCase):
    def setUp(self):
        self.url = reverse('digitalglarus:contact')
        self.data = {
            'name': 'test',
            'email': 'test@gmail.com',
            'phone_number': '32123123123123',
            'message': 'This is a message',
        }

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_any_user_should_contact_us(self):
        response = self.client.post(self.url, self.data, follow=True)
        self.assertEqual(response.status_code, 200)


class ViewsTest(CMSTestCase):
    def setUp(self):
        self.page1 = create_page(
            'home', 'home_digitalglarus.html', published=True,
            language='en-us'
        )
        self.page2 = create_page(
            'about', 'about.html', published=True, language='en-us',
            slug='about'
        )

    def test_digitalglarus_templates(self):
        res1 = self.client.get('/en-us/')
        self.assertContains(res1, 'Digital Glarus', status_code=200)
        res2 = self.client.get('/en-us/cms/about/')
        self.assertEqual(res2.status_code, 200)


class MembershipPricingViewTest(BaseTestCase):

    def setUp(self):
        super(MembershipPricingViewTest, self).setUp()

        self.membership_type = mommy.make(MembershipType)
        self.url = reverse('digitalglarus:membership_pricing')
        self.view = MembershipPricingView
        self.expected_template = 'digitalglarus/membership_pricing.html'

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        # Anonymous user should get data
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.context['membership_type'], self.membership_type
        )
        self.assertTemplateUsed(response, self.expected_template)


class MembershipPaymentViewTest(BaseTestCase):

    def setUp(self):
        super(MembershipPaymentViewTest, self).setUp()

        self.membership_type = mommy.make(MembershipType)
        self.url = reverse('digitalglarus:membership_payment')
        self.view = MembershipPaymentView
        self.expected_template = 'digitalglarus/membership_payment.html'

        # post data
        self.billing_address = {
            'street_address': 'street name',
            'city': 'MyCity',
            'postal_code': '32123123123123',
            'country': 'VE',
            'token': 'a23kfmslwxhkwis',
            'membership_type': self.membership_type.id
        }

    def test_url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):

        # Anonymous user should get redirect to login
        response = self.client.get(self.url)
        expected_url = "%s?next=%s" % (
            reverse('digitalglarus:signup'),
            reverse('digitalglarus:membership_payment')
        )
        self.assertRedirects(response, expected_url=expected_url,
                             status_code=302, target_status_code=200)

        # Logged user should get the page
        response = self.customer_client.get(self.url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['stripe_key'],
                         settings.STRIPE_API_PUBLIC_KEY)
        self.assertEqual(response.context['membership_type'],
                         self.membership_type)

    @mock.patch('utils.stripe_utils.StripeUtils.create_customer')
    def test_post(self, stripe_mocked_call):

        # Anonymous user should get redirect to login
        # response = self.client.post(self.url)
        # expected_url = "%s?next=%s" % (reverse('digitalglarus:signup'),
        #                                reverse('digitalglarus:membership_payment'))
        # self.assertRedirects(response, expected_url=expected_url,
        #                      status_code=302, target_status_code=200)

        # Customer user should be able to pay
        stripe_mocked_call.return_value = {
            'paid': True,
            'response_object': self.stripe_mocked_customer,
            'error': None
        }
        response = self.customer_client.post(self.url, self.billing_address)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(
            StripeCustomer.objects.filter(
                user__email=self.customer.email
            ).exists()
        )
        stripe_customer = StripeCustomer.objects.get(
            user__email=self.customer.email
        )
        self.assertEqual(stripe_customer.user, self.customer)
        # self.assertTrue(MembershipOrder.objects.filter(customer=stripe_customer).exists())
        # membership_order = MembershipOrder.objects.filter(
        #     customer=stripe_customer
        # ).first()
        # session_data = {
        #     'membership_price':
        #         membership_order.membership.type.first_month_price,
        #     'membership_dates':
        #         membership_order.membership.type.first_month_formated_range
        # }
        # self.assertEqual(session_data.get('membership_price'),
        #                  self.session_data.get('membership_price'))
        # self.assertEqual(session_data.get('membership_dates'),
        #                  self.session_data.get('membership_dates'))

        # self.assertTrue(HostingOrder.objects.filter(customer=stripe_customer).exists())
        # hosting_order = HostingOrder.objects.filter(customer=stripe_customer)[0]
        # vm_plan = {
        #  'cores': hosting_order.vm_plan.cores,
        #     'memory': hosting_order.vm_plan.memory,
        #     'disk_size': hosting_order.vm_plan.disk_size,
        #     'price': hosting_order.vm_plan.price,
        #     'hosting_company': hosting_order.vm_plan.vm_type.hosting_company,
        #     'configuration': hosting_order.vm_plan.configuration
        # }
        # self.assertEqual(vm_plan, self.session_data.get('vm_specs'))


class LoginViewTest(TestCase):

    def setUp(self):
        self.url = reverse('digitalglarus:login')
        self.view = LoginView
        self.expected_template = 'digitalglarus/login.html'
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
        self.url = reverse('digitalglarus:signup')
        self.expected_template = 'digitalglarus/signup.html'
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
        response = self.client.post(
            self.url, data=self.signup_data, follow=True
        )
        self.user = CustomUser.objects.get(email=self.signup_data.get('email'))
        self.assertEqual(response.context['user'], self.user)
        self.assertEqual(response.status_code, 200)


class PasswordResetViewTest(BaseTestCase):

    def setUp(self):
        super(PasswordResetViewTest, self).setUp()

        self.url = reverse('digitalglarus:reset_password')
        self.view = PasswordResetView
        self.expected_template = 'digitalglarus/reset_password.html'
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
        context = self.setup_view(self.view()).\
            test_generate_email_context(self.user)
        self.assertEqual(context.get('user'), self.user)
        self.assertEqual(context.get('site_name'), 'ungleich')
        self.assertEqual(len(context.get('token')), 24)


class PasswordResetConfirmViewTest(BaseTestCase):

    def setUp(self):
        super(PasswordResetConfirmViewTest, self).setUp()

        self.view = PasswordResetConfirmView
        self.expected_template = 'digitalglarus/confirm_reset_password.html'
        self.user = mommy.make('membership.CustomUser')
        self.password = 'fake_password'
        self.user.set_password(self.password)
        self.user.save()

        self.token = default_token_generator.make_token(self.user)
        self.uid = urlsafe_base64_encode(force_bytes(self.user.pk))
        self.url = reverse('digitalglarus:reset_password_confirm',
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

    def test_post(self):
        response = self.client.post(self.url, data=self.post_data, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTrue(not response.context['form'].errors)

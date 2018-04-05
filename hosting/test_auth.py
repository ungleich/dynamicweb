from django.conf import settings
from django.contrib.auth.hashers import make_password
from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase, Client
from django.test.client import RequestFactory
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.utils.translation import activate
from django.utils.translation import ugettext_lazy as _

from membership.models import CustomUser

from model_mommy import mommy
from hosting.forms import HostingUserLoginForm, HostingUserSignupForm
from utils.forms import PasswordResetRequestForm, SetPasswordForm


class RegistrationUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.resp = self.client.post(
            reverse('hosting:signup'),
            data={
                'name': 'test',
                'email': 'test@example.com',
                'password': 'secret',
                'confirm_password': 'secret'
            }
        )

    def test_login_form_language(self):
        activate('de')
        login_resp = self.client.get(reverse("hosting:signup"))
        self.assertEqual(login_resp._headers['content-language'][1], 'de')

    def test_login_redirection(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        self.client.get(
            reverse(
                'hosting:validate',
                kwargs={'validate_slug': new_user.validation_slug}
            )
        )
        login_resp = self.client.login(email=new_user.email, password='secret')
        self.assertEqual(login_resp, True)
        redirect_resp = self.client.post(
            reverse('hosting:login'),
            data={
                'email': new_user.email,
                'password': 'secret'
            }
        )
        self.assertRedirects(redirect_resp, reverse('hosting:dashboard'))

    def test_registration(self):
        self.assertRedirects(self.resp, reverse('hosting:signup-validate'))
        new_user = CustomUser.objects.get(email='test@example.com')
        self.failUnless(new_user.check_password('secret'))
        self.assertEqual(new_user.email, 'test@example.com')
        self.assertEqual(len(mail.outbox), 1)

    def test_activation(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        self.client.get(
            reverse(
                'hosting:validate',
                kwargs={
                    'validate_slug': new_user.validation_slug
                }
            )
        )
        self.assertEqual(CustomUser.validate_url(new_user.validation_slug), True)
        self.assertEqual(len(mail.outbox), 2)

    def test_activation_with_wrong_validation_slug(self):
        CustomUser.objects.get(email='test@example.com')
        wrong_validation_slug = make_password(None)
        self.client.get(
            reverse(
                'hosting:validate',
                kwargs={
                    'validate_slug': wrong_validation_slug
                }
            )
        )
        self.assertEqual(CustomUser.validate_url(wrong_validation_slug), False)

    def test_reset_password(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        request = self.factory.get(reverse('hosting:signup'))
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        context = {
            'user': new_user,
            'token': default_token_generator.make_token(new_user),
            'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
            'site_name': 'test_site',
            'base_url': base_url
        }
        resp = self.client.post(
            reverse('hosting:reset_password'),
            data={
                'email': 'test@example.com',
                'subject': _('Password Reset'),
                'context': context,
                'template_name': 'password_reset_email',
                'template_path': 'hosting/emails/'
            }
        )
        self.assertEqual(len(mail.outbox), 2)
        self.assertRedirects(resp, reverse('hosting:login'))

    def test_resend_activation_link(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        context = {
            'base_url': "http://localhost:8000/",
            'activation_link': reverse_lazy(
                'hosting:validate',
                kwargs={'validate_slug': new_user.validation_slug}
            ),
            'dcl_text': 'Data Center Light',
        }
        resp = self.client.post(
            reverse('hosting:resend_activation_link'),
            data={
                'subject': 'Data Center Light Account Activation Test',
                'to': 'test@example.com',
                'context': context,
                'template_name': 'hosting/reset_password.html',
                'template_path': 'datacenterlight/emails/',
                'from_address': '(Data Center Light) Data Center Light Support <support@datacenterlight.ch>'
            }
        )
        self.assertEqual(len(mail.outbox), 1)
        self.assertEqual(200, resp.status_code)


class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.factory = RequestFactory()
        self.data = {
            'name': 'test',
            'email': 'test@example.com',
            'password': 'secret',
            'confirm_password': 'secret'
        }
        self.resp = self.client.post(
            reverse('hosting:signup'),
            data=self.data
        )

    def test_mail_receiver_sender(self):
        email = mail.outbox[0]
        self.assertEqual(email.to[0], 'test@example.com')
        self.assertEqual(email.from_email, settings.DCL_SUPPORT_FROM_ADDRESS)

    def test_mail_type_en_content_to_user(self):
        activate('en-us')
        request = self.factory.get(reverse('hosting:signup'))
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        new_user = CustomUser.objects.get(email='test@example.com')
        template_path = 'datacenterlight/emails/'
        template_name = 'user_activation'
        email_data = {
            'subject': '{dcl_text} {account_activation}'.format(
                dcl_text=settings.DCL_TEXT,
                account_activation=_('Account Activation')
            ),
            'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': new_user.email,
            'context': {
                'base_url': base_url,
                'activation_link': reverse(
                    'hosting:validate',
                    kwargs={
                        'validate_slug': new_user.validation_slug
                    }
                ),
                'dcl_text': settings.DCL_TEXT
            },
            'template_name': template_name,
            'template_path': template_path
        }
        template_full_path = '%s%s' % (template_path, template_name)
        text_content = render_to_string('%s.txt' % template_full_path, email_data['context'])
        html_content = render_to_string('%s.html' % template_full_path, email_data['context'])
        email = EmailMultiAlternatives(email_data['subject'], text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [email_data.get('to', 'info@ungleich.ch')]
        email.send()
        self.assertEqual(mail.outbox[1].body, text_content)
        self.assertEqual(mail.outbox[1].alternatives[0][0], html_content)

    def test_mail_type_de_content_to_user(self):
        activate('de')
        request = self.factory.get(reverse('hosting:signup'))
        base_url = "{0}://{1}".format(request.scheme, request.get_host())
        new_user = CustomUser.objects.get(email='test@example.com')
        template_path = 'datacenterlight/emails/'
        template_name = 'user_activation'
        email_data = {
            'subject': '{dcl_text} {account_activation}'.format(
                dcl_text=settings.DCL_TEXT,
                account_activation=_('Account Activation')
            ),
            'from_address': settings.DCL_SUPPORT_FROM_ADDRESS,
            'to': new_user.email,
            'context': {
                'base_url': base_url,
                'activation_link': reverse(
                    'hosting:validate',
                    kwargs={
                        'validate_slug': new_user.validation_slug
                    }
                ),
                'dcl_text': settings.DCL_TEXT
            },
            'template_name': template_name,
            'template_path': template_path
        }
        template_full_path = '%s%s' % (template_path, template_name)
        text_content = render_to_string('%s.txt' % template_full_path, email_data['context'])
        html_content = render_to_string('%s.html' % template_full_path, email_data['context'])
        email = EmailMultiAlternatives(email_data['subject'], text_content)
        email.attach_alternative(html_content, "text/html")
        email.to = [email_data.get('to', 'info@ungleich.ch')]
        email.send()
        self.assertEqual(mail.outbox[1].body, text_content)
        self.assertEqual(mail.outbox[1].alternatives[0][0], html_content)
        email_text = email.alternatives[0][0]
        if "You can activate your Data Center Light account" in email_text:
            language = 'en-us'
        else:
            language = "de"
        self.assertEqual(language, 'en-us')
        self.assertEqual(language, 'de')


class UserLoginFormTest(TestCase):
    def setUp(self):
        password = 'user_password'
        self.user = mommy.make('CustomUser', validated=1)
        self.user.set_password(password)
        self.user.save()
        self.completed_data = {
            'email': self.user.email,
            'password': password
        }
        self.incorrect_user_data = {
            'email': 'test',
            'password': password
        }
        self.incorrect_password_data = {
            'email': self.user.email,
            'password': 'test'
        }

    def test_user_login_valid_form(self):
        form = HostingUserLoginForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_user_login_user_invalid_form(self):
        form = HostingUserLoginForm(data=self.incorrect_user_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['User does not exist']
        })

    def test_user_login_password_invalid_form(self):
        form = HostingUserLoginForm(data=self.incorrect_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            '__all__': ['Your username and/or password were incorrect.']
        })

    def test_user_login_blank_data_en_message(self):
        activate('en-us')
        form = HostingUserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['This field is required.'],
            'password': ['This field is required.']
        })

    def test_user_login_blank_data_de_message(self):
        activate('de')
        form = HostingUserLoginForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'email': ['Dieses Feld ist erforderlich.'],
            'password': ['Dieses Feld ist erforderlich.']
        })


class UserSignupFormTest(TestCase):
    def setUp(self):
        self.completed_data = {
            'name': 'test name',
            'email': 'test@ungleich.ch',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }
        self.incorrect_password_data = {
            'name': 'test name',
            'email': 'test@ungleich.ch',
            'password': 'test_password',
            'confirm_password': 'another_test_password'
        }
        self.incorrect_data = {
            'email': 'test',
        }

    def test_user_signup_valid_form(self):
        form = HostingUserSignupForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_user_signup_invalid_form(self):
        form = HostingUserSignupForm(data=self.incorrect_password_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'confirm_password': ["Passwords don't match"]
        })

    def test_user_signup_password_invalid_form_en_message(self):
        activate('en-us')
        form = HostingUserSignupForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['Enter a valid email address.'],
            'password': ['This field is required.'],
            'confirm_password': ['This field is required.']
        })

    def test_user_signup_password_invalid_form_de_message(self):
        activate('de')
        form = HostingUserSignupForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['Dieses Feld ist erforderlich.'],
            'email': ['Gib eine gültige E-Mail Adresse an.'],
            'password': ['Dieses Feld ist erforderlich.'],
            'confirm_password': ['Dieses Feld ist erforderlich.']
        })

    def test_user_signup_blank_data_en_message(self):
        activate('en-us')
        form = HostingUserSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['This field is required.'],
            'email': ['This field is required.'],
            'password': ['This field is required.'],
            'confirm_password': ['This field is required.']
        })

    def test_user_signup_blank_data_de_message(self):
        activate('de')
        form = HostingUserSignupForm(data={})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors, {
            'name': ['Dieses Feld ist erforderlich.'],
            'email': ['Dieses Feld ist erforderlich.'],
            'password': ['Dieses Feld ist erforderlich.'],
            'confirm_password': ['Dieses Feld ist erforderlich.']
        })


class PasswordResetRequestFormTest(TestCase):
    def setUp(self):
        self.user = mommy.make('CustomUser')
        self.completed_data = {
            'email': self.user.email,
        }
        self.incorrect_data = {
            'email': 'test',
        }

    def test_valid_form(self):
        form = PasswordResetRequestForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = PasswordResetRequestForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())


class SetPasswordFormTest(TestCase):
    def setUp(self):
        self.completed_data = {
            'new_password1': 'new_password',
            'new_password2': 'new_password',
        }
        self.incorrect_data = {
            'email': 'test',
        }

    def test_valid_form(self):
        form = SetPasswordForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = SetPasswordForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())

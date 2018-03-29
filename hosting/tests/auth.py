from django.contrib.auth.tokens import default_token_generator
from django.core import mail
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase, Client
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.translation import ugettext_lazy as _

from membership.models import CustomUser


class RegistrationUnitTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.resp = self.client.post(
                reverse('hosting:signup'), 
                data={
                        'name': 'test', 
                        'email': 'test@example.com', 
                        'password': 'secret', 
                        'confirm_password': 'secret'
                    }
            )

    def test_login_redirection(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        activation_resp = self.client.get(
                reverse(
                        'hosting:validate', 
                        kwargs={
                                'validate_slug': new_user.validation_slug
                            }
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
        resp = self.client.get(
                reverse(
                        'hosting:validate', 
                        kwargs={
                                'validate_slug': new_user.validation_slug
                            }
                    )
            )
        self.assertEqual(200, resp.status_code)

    def test_reset_password(self):
        new_user = CustomUser.objects.get(email='test@example.com')
        context = {
                'user': new_user,
                'token': default_token_generator.make_token(new_user),
                'uid': urlsafe_base64_encode(force_bytes(new_user.pk)),
                'site_name': 'test_site',
                'base_url': "http://localhost:8000/"
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
        context = {'base_url': "http://localhost:8000/",
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
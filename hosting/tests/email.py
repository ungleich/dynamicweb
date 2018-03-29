from django.conf import settings
from django.core import mail
from django.core.mail import EmailMultiAlternatives
from django.core.urlresolvers import reverse
from django.template.loader import render_to_string
from django.test import TestCase, Client
from django.utils.translation import ugettext_lazy as _

from membership.models import CustomUser


class EmailTest(TestCase):
    def setUp(self):
        self.client = Client()
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

    def test_mail_type_content_to_user(self):
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
                'context': {'base_url': "http://localhost:8000/",
                            'activation_link': reverse(
                                'hosting:validate',
                                kwargs={
                                    'validate_slug': new_user.validation_slug}),
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
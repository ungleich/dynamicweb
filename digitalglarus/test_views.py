from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve


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

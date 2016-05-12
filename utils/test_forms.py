from django.test import TestCase
from .forms import ContactUsForm, BillingAddressForm


class ContactUsFormTest(TestCase):

    def setUp(self):
        self.completed_data = {
            'name': 'test',
            'email': 'test@gmail.com',
            'phone_number': '32123123123123',
            'message': 'This is a message',
        }

        self.incompleted_data = {
            'name': 'test',
        }

    def test_valid_form(self):
        form = ContactUsForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = ContactUsForm(data=self.incompleted_data)
        self.assertFalse(form.is_valid())


class BillingAddressFormTest(TestCase):

    def setUp(self):
        self.completed_data = {
            'street_address': 'street name',
            'city': 'MyCity',
            'postal_code': '32123123123123',
            'country': 'VE',
            'token': 'a23kfmslwxhkwis'
        }

        self.incompleted_data = {
            'street_address': 'test',
        }

    def test_valid_form(self):
        form = BillingAddressForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = BillingAddressForm(data=self.incompleted_data)
        self.assertFalse(form.is_valid())

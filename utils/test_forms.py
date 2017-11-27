from django.test import TestCase
from .forms import ContactUsForm, BillingAddressForm, PasswordResetRequestForm,\
    SetPasswordForm

from model_mommy import mommy


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
        # self.user = mommy.make('CustomUser')
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
            'cardholder_name': 'test',
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

import datetime

from django.http import HttpResponseRedirect
from django.test import TestCase, Client

from model_mommy import mommy

from .forms import HostingUserLoginForm, HostingUserSignupForm, \
    generate_ssh_key_name


class HostingUserLoginFormTest(TestCase):

    def setUp(self):
        password = 'user_password'
        self.user = mommy.make('CustomUser')

        self.user.set_password(password)
        self.user.validated = 1
        self.user.save()
        self.completed_data = {
            'email': self.user.email,
            'password': password
        }

        self.incorrect_data = {
            'email': 'test',
        }

    def test_clean_form(self):
        form = HostingUserLoginForm(data=self.completed_data)
        self.user.validated = 0
        self.user.save()
        self.assertFalse(form.is_valid())

    def test_valid_form(self):
        form = HostingUserLoginForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = HostingUserLoginForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())


class HostingUserSignupFormTest(TestCase):

    def setUp(self):
        self.completed_data = {
            'name': 'test name',
            'email': 'test@ungleich.com',
            'password': 'test_password',
            'confirm_password': 'test_password'
        }

        self.incorrect_data = {
            'email': 'test',
        }

    def test_valid_form(self):
        form = HostingUserSignupForm(data=self.completed_data)
        self.assertTrue(form.is_valid())

    def test_invalid_form(self):
        form = HostingUserSignupForm(data=self.incorrect_data)
        self.assertFalse(form.is_valid())

class GenerateSShKeynameTest(TestCase):

    def test_generate_ssh_keyname_test(self):
        name = 'dcl-generated-key-' + datetime.datetime.now().strftime('%m%d%y%H%M')
        self.assertEqual(generate_ssh_key_name(), name)


class UserHostingKeyFormTest(TestCase):

    def setUp(self):
        self.client = Client()
        password = 'user_password'
        self.user = mommy.make('CustomUser')

        self.user.set_password(password)
        self.user.validated = 1
        self.user.save()

        self.completed_data = {
            'private_key': 'private_key',
            'public_key': 'public_key',
            'user': self.user,
            'name': 'name',
            'generate': ''
        }

    def test_clean_form(self):
        response = self.client.post('/hosting/create_ssh_key/', self.completed_data)
        self.assertIsInstance(response, HttpResponseRedirect)


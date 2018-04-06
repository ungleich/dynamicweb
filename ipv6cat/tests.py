from django.test import TestCase
from ipv6cat.forms import CatCreateForm
# Create your tests here.

class CatCreateFormTest(TestCase):
    def setUp(self):
        self.complete_data = {
            'title': 'test',
            'description': 'test',
            'image': 'test.jpg'
        }
        self.incomplete_data = {
            'title': 'test'
        }

    def test_cat_create(self):
        form = CatCreateForm(data=self.complete_data)
        self.assertTrue(form.is_valid())

    def test_cat_create_invalid(self):
        form = CatCreateForm(data=self.incomplete_data)
        self.assertFalse(form.is_valid())
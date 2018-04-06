from django.test import TestCase
from ipv6cat.forms import CatCreateForm


# Create your tests here.
class CatCreateFormTest(TestCase):
    def setUp(self):
        self.incomplete_data = {'title': 'test'}

    def test_cat_create_invalid(self):
        form = CatCreateForm(data=self.incomplete_data)
        self.assertFalse(form.is_valid())

from django.test import TestCase
from django.core.files.uploadedfile import SimpleUploadedFile
from ipv6cat.forms import CatCreateForm


# Create your tests here.
class CatCreateFormTest(TestCase):
    def setUp(self):
        self.complete_data = {
            'title': 'test',
            'description': 'test'
        }
        self.incomplete_data = {'title': 'test'}

    def test_cat_create(self):
        upload_file = open('path/to/file', 'rb')
        img_dict = {'image': SimpleUploadedFile(upload_file.name, upload_file.read())}
        form = CatCreateForm(data=self.complete_data, files=img_dict)
        self.assertTrue(form.is_valid())

    def test_cat_create_invalid(self):
        form = CatCreateForm(data=self.incomplete_data)
        self.assertFalse(form.is_valid())

from django.test import TestCase
from .templatetags.custom_tags import change_lang, get_value_from_dict


class CustomeTemplateTagTest(TestCase):

    def change_lang_test(self):

        class TestRequest:

            def __init__(self, path):
                self.path=path
        test_request = TestRequest(path='/test/path')
        context = {'request': test_request}
        self.assertEqual(change_lang(context=context), 'test/path')

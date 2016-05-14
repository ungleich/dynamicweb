import json

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from cms.test_utils.testcases import CMSTestCase
from cms.api import create_page


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


class ViewsTest(CMSTestCase):
    def setUp(self):
        self.page1 = create_page('home', 'home_digitalglarus.html', published=True, language='en-us')
        self.page2 = create_page('about', 'about.html', published=True, language='en-us', slug='about')

    def test_digitalglarus_templates(self):
        res1 = self.client.get('/en-us/')
        self.assertContains(res1, 'Digital Glarus', status_code=200)
        res2 = self.client.get('/en-us/about/')
        self.assertEqual(res2.status_code, 200)


class CalendarApiTestCase(TestCase):
    def test_api_response(self):
        calendar_api_url_1 = reverse('digitalglarus:calendar_api_1', kwargs={'month': '3', 'year': '2016'})
        res1 = self.client.get(calendar_api_url_1)
        pd = json.loads(res1.content.decode('utf-8'))
        self.assertEqual(pd['month'], '3')
        self.assertEqual(pd['year'], '2016')

        # TODO:check post
        # calendar_api_url = reverse('digitalglarus:calendar_api')
        # res = self.client.get(calendar_api_url)

from django.test import TestCase
from django.core.urlresolvers import reverse
from django.core.urlresolvers import resolve
from .models import VirtualMachineType
from .views import DjangoHostingView, RailsHostingView, NodeJSHostingView


class ProcessVMSelectionTestMixin(object):

    def url_resolve_to_view_correctly(self):
        found = resolve(self.url)
        self.assertEqual(found.func.__name__, self.view.__name__)

    def test_get(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.view.get_context_data(), self.expected_context)
        self.assertEqual(response.context['hosting'], self.expected_context['hosting'])
        self.assertTemplateUsed(response, self.expected_template)

    def test_anonymous_post(self):
        response = self.client.post(self.url)
        self.assertRedirects(response, expected_url=reverse('hosting:login'),
                             status_code=302, target_status_code=200)


class DjangoHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('django.hosting')
        self.view = DjangoHostingView()
        self.expected_template = 'hosting/django.html'
        self.expected_context = {
            'hosting': "django",
            'hosting_long': "Django",
            'domain': "django-hosting.ch",
            'google_analytics': "UA-62285904-6",
            'email': "info@django-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class RailsHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('rails.hosting')
        self.view = RailsHostingView()
        self.expected_template = 'hosting/rails.html'
        self.expected_context = {
            'hosting': "rails",
            'hosting_long': "Ruby On Rails",
            'domain': "rails-hosting.ch",
            'google_analytics': "UA-62285904-5",
            'email': "info@rails-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }


class NodeJSHostingViewTest(TestCase, ProcessVMSelectionTestMixin):

    def setUp(self):
        self.url = reverse('node.hosting')
        self.view = NodeJSHostingView()
        self.expected_template = 'hosting/nodejs.html'
        self.expected_context = {
            'hosting': "nodejs",
            'hosting_long': "NodeJS",
            'domain': "node-hosting.ch",
            'google_analytics': "UA-62285904-7",
            'email': "info@node-hosting.ch",
            'vm_types': VirtualMachineType.get_serialized_vm_types(),
        }

from django.core.management.base import BaseCommand
from datacenterlight.cms_models import CMSIntegration


class Command(BaseCommand):
    help = '''Creates cms integration objects for datacenterlight'''

    def handle(self, *args, **options):
        self.create_cms_integration()

    def create_cms_integration(self, site=None):
        obj, created = CMSIntegration.objects.get_or_create(
            name='default', domain=site
        )
        domain_name = site.domain if site else 'All Sites'
        if created:
            print('created the default CMSIntegration object for', domain_name)
        else:
            print(
                'default CMSIntegration object already exists for', domain_name
            )

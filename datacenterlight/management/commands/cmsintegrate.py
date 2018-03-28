from django.core.management.base import BaseCommand
from datacenterlight.cms_models import CMSIntegration


class Command(BaseCommand):
    help = '''Creates cms integration objects for datacenterlight'''

    def handle(self, *args, **options):
        obj, created = CMSIntegration.objects.get_or_create(name='default')
        if created:
            print('created the default CMSIntegration object')
        else:
            print('default CMSIntegration object already exists')

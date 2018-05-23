from django.core.management.base import BaseCommand
from opennebula_api.models import OpenNebulaManager
from datacenterlight.models import VMTemplate
import logging

logger = logging.getLogger(__name__)


class Command(BaseCommand):
    help = '''Fetches the VM templates from OpenNebula and populates the dcl
            VMTemplate model'''

    def get_templates(self, manager, prefix):
        templates = manager.get_templates('%s-' % prefix)
        dcl_vm_templates = []
        for template in templates:
            template_name = template.name.lstrip('%s-' % prefix)
            template_id = template.id
            dcl_vm_template = VMTemplate.create(
                template_name, template_id, prefix
            )
            dcl_vm_templates.append(dcl_vm_template)
        return dcl_vm_templates

    def handle(self, *args, **options):
        try:
            manager = OpenNebulaManager()
            dcl_vm_templates = []
            dcl_vm_templates.extend(
                self.get_templates(manager, VMTemplate.PUBLIC)
            )
            dcl_vm_templates.extend(
                self.get_templates(manager, VMTemplate.IPV6)
            )

            old_vm_templates = VMTemplate.objects.all()
            old_vm_templates.delete()

            for dcl_vm_template in dcl_vm_templates:
                dcl_vm_template.save()
        except Exception as e:
            logger.error('Error connecting to OpenNebula. Error Details: '
                         '{err}'.format(err=str(e)))

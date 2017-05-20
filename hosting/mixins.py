from django.shortcuts import redirect
from django.core.urlresolvers import reverse

from opennebula_api.serializers import VirtualMachineTemplateSerializer
from opennebula_api.models import OpenNebulaManager


class ProcessVMSelectionMixin(object):

    def post(self, request, *args, **kwargs):

        template_id = int(request.POST.get('vm_template_id'))
        template = OpenNebulaManager().get_template(template_id)
        data = VirtualMachineTemplateSerializer(template).data
        request.session['template'] = data

        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')
            return redirect(reverse('hosting:login'))
        return redirect(reverse('hosting:payment'))

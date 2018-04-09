from django.shortcuts import redirect
from django.conf import settings
from django.core.urlresolvers import reverse

from opennebula_api.serializers import VirtualMachineTemplateSerializer
from opennebula_api.models import OpenNebulaManager

from .models import HostingPlan


class ProcessVMSelectionMixin(object):

    def post(self, request, *args, **kwargs):

        template_id = int(request.POST.get('vm_template_id'))
        configuration_id = int(request.POST.get('configuration'))
        template = OpenNebulaManager().get_template(template_id)
        data = VirtualMachineTemplateSerializer(template).data
        configuration = HostingPlan.objects.get(id=configuration_id)

        request.session['template'] = data
        request.session['specs'] = configuration.serialize()

        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')
            return redirect(reverse('hosting:login'))
        return redirect(reverse('hosting:payment'))


class HostingContextMixin(object):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['MULTISITE_CMS_FALLBACK'] = settings.MULTISITE_CMS_FALLBACK
        return context

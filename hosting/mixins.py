from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class ProcessVMSelectionMixin(object):

    def post(self, request, *args, **kwargs):
        #configuration = request.POST.get('configuration')
        #configuration_display = dict(VirtualMachinePlan.VM_CONFIGURATION).get(configuration)
        vm_template_id = request.POST.get('vm_template_id')
        vm_specs.update({
            'configuration_display': configuration_display,
            'configuration': configuration,
            'vm_template_id': vm_template_id
        })
        request.session['vm_specs'] = vm_specs
        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')
            return redirect(reverse('hosting:login'))
        return redirect(reverse('hosting:payment'))

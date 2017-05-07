from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import VirtualMachinePlan, VirtualMachineType


class ProcessVMSelectionMixin(object):

    def post(self, request, *args, **kwargs):
        configuration = request.POST.get('configuration')
        configuration_display = dict(VirtualMachinePlan.VM_CONFIGURATION).get(configuration)
        vm_template = request.POST.get('vm_template')
        vm_type = VirtualMachineType.objects.get(id=vm_template)
        vm_specs = vm_type.get_specs()
        vm_specs.update({
            'configuration_display': configuration_display,
            'configuration': configuration,
            'final_price': vm_type.final_price,
            'vm_template': vm_template
        })
        # vm_specs = {
        #     # 'cores': request.POST.get('cores'),
        #     # 'memory': request.POST.get('memory'),
        #     # 'disk_size': request.POST.get('disk_space'),
        #     # 'hosting_company': request.POST.get('hosting_company'),
        #     # 'location_code': request.POST.get('location_code'),
        #     # 'configuration': hosting,
        #     # 'configuration_detail': configuration_detail,
        #     'final_price': request.POST.get('final_price')
        # }
        request.session['vm_specs'] = vm_specs
        if not request.user.is_authenticated():
            request.session['vm_specs'] = vm_specs
            request.session['next'] = reverse('hosting:payment')
            return redirect(reverse('hosting:login'))
        return redirect(reverse('hosting:payment'))

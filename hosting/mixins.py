from django.shortcuts import redirect
from django.core.urlresolvers import reverse


class ProcessVMSelectionMixin(object):

    def post(self, request, *args, **kwargs):
        vm_specs = {
            'cores': request.POST.get('cores'),
            'memory': request.POST.get('memory'),
            'disk_size': request.POST.get('disk_space'),
            'hosting_company': request.POST.get('hosting_company'),
            'hosting_company_name': request.POST.get('hosting_company_name'),
            'final_price': request.POST.get('final_price')
        }
        request.session['vm_specs'] = vm_specs
        if not request.user.is_authenticated():
            request.session['vm_specs'] = vm_specs
            return redirect(reverse('hosting:login'))
        return redirect(reverse('hosting:payment'))

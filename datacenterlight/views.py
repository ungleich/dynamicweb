from django.views.generic import FormView, CreateView, TemplateView
from django.http import HttpResponseRedirect
from .forms import BetaAccessForm
from .models import BetaAccess, BetaAccessVMType, BetaAccessVM
from django.contrib import messages
from django.core.urlresolvers import reverse_lazy, reverse
from utils.mailer import BaseEmail
from django.shortcuts import render
from django.shortcuts import redirect

from opennebula_api.models import OpenNebulaManager
from opennebula_api.serializers import VirtualMachineTemplateSerializer

class LandingProgramView(TemplateView):
    template_name = "datacenterlight/landing.html"

class PricingView(TemplateView):
    template_name = "datacenterlight/pricing.html"

    def get(self, request, *args, **kwargs):
        try:
            manager = OpenNebulaManager()
            templates = manager.get_templates()

            context = {
                'templates': VirtualMachineTemplateSerializer(templates, many=True).data,
            }
        except:
            messages.error( request,
                'We could not load the VM templates due to a backend connection \
                error. Please try again in a few minutes'
                )
            context = {
                'error' : 'connection'
                    }

        return render(request, self.template_name, context)


    def post(self, request):

        cores = request.POST.get('cpu')
        memory = request.POST.get('ram')
        storage = request.POST.get('storage')
        price = request.POST.get('total')

        template_id = int(request.POST.get('config'))

        manager = OpenNebulaManager()
        template = manager.get_template(template_id)

        request.session['template'] = VirtualMachineTemplateSerializer(template).data

        if not request.user.is_authenticated():
            request.session['next'] = reverse('hosting:payment')

        request.session['specs'] = { 
            'cpu':cores,
            'memory': memory,
            'disk_size': storage,
            'price': price,
        }

        return redirect(reverse('hosting:payment'))


class BetaAccessView(FormView):
    template_name = "datacenterlight/beta_access.html"
    form_class = BetaAccessForm  
    success_message = "Thank you, we will contact you as soon as possible"

    def form_valid(self, form):

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'to': form.cleaned_data.get('email'),
            'context': context,
            'template_name': 'request_access_confirmation',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        context.update({
            'email': form.cleaned_data.get('email')
        })

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return render(self.request, 'datacenterlight/beta_success.html', {})

class BetaProgramView(CreateView):
    template_name = "datacenterlight/beta.html"
    model = BetaAccessVM
    fields = '__all__'
    # form_class = BetaAccessForm
    # success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def get_success_url(self):
        success_url = reverse('datacenterlight:beta')
        success_url += "#success"
        return success_url

    def get_context_data(self, **kwargs):
        vms = BetaAccessVMType.objects.all()
        context = super(BetaProgramView, self).get_context_data(**kwargs)

        # templates = OpenNebulaManager().get_templates()
        # data = VirtualMachineTemplateSerializer(templates, many=True).data

        context.update({
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host()),
            'vms': vms
        })
        return context

    def post(self, request, *args, **kwargs):
        data = request.POST
        vms = BetaAccessVM.create(data)

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host()),
            'email': data.get('email'),
            'name': data.get('name'),
            'vms': vms
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_beta_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return HttpResponseRedirect(self.get_success_url())
        # return super(BetaProgramView, self).form_valid(form)


        

    # def form_valid(self, form):

    #     context = {
    #         'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
    #     }

    #     email_data = {
    #         'subject': 'DatacenterLight Beta Access Request',
    #         'to': form.cleaned_data.get('email'),
    #         'context': context,
    #         'template_name': 'request_access_confirmation',
    #         'template_path': 'datacenterlight/emails/'
    #     }
    #     email = BaseEmail(**email_data)
    #     email.send()

    #     context.update({
    #         'email': form.cleaned_data.get('email')
    #     })

    #     email_data = {
    #         'subject': 'DatacenterLight Beta Access Request',
    #         'to': 'info@ungleich.ch',
    #         'context': context,
    #         'template_name': 'request_access_notification',
    #         'template_path': 'datacenterlight/emails/'
    #     }
    #     email = BaseEmail(**email_data)
    #     email.send()

    #     messages.add_message(self.request, messages.SUCCESS, self.success_message)
    #     return super(IndexView, self).form_valid(form)


class IndexView(CreateView):
    template_name = "datacenterlight/home.html"
    model = BetaAccess
    form_class = BetaAccessForm
    success_url = "/datacenterlight#requestform"
    success_message = "Thank you, we will contact you as soon as possible"

    def get_success_url(self):
        success_url = reverse('datacenterlight:index')
        success_url += "#requestform"
        return success_url

    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context.update({
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        })
        return context

    def form_valid(self, form):

        context = {
            'base_url': "{0}://{1}".format(self.request.scheme, self.request.get_host())
        }

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'to': form.cleaned_data.get('email'),
            'context': context,
            'template_name': 'request_access_confirmation',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        context.update({
            'email': form.cleaned_data.get('email')
        })

        email_data = {
            'subject': 'DatacenterLight Beta Access Request',
            'to': 'info@ungleich.ch',
            'context': context,
            'template_name': 'request_access_notification',
            'template_path': 'datacenterlight/emails/'
        }
        email = BaseEmail(**email_data)
        email.send()

        messages.add_message(self.request, messages.SUCCESS, self.success_message)
        return super(IndexView, self).form_valid(form)



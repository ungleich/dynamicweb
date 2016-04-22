
from django.shortcuts import get_object_or_404, render
from django.core.urlresolvers import reverse_lazy, reverse

from django.views.generic import View, CreateView, FormView
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login

from membership.models import CustomUser
from .models import RailsBetaUser, VirtualMachineType
from .forms import HostingUserSignupForm, HostingUserLoginForm


class VMPricingView(View):
    template_name = "hosting/pricing.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, request)


class DjangoHostingView(View):
    template_name = "hosting/django.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["hosting"] = "django"
        context["hosting_long"] = "Django"
        context["domain"] = "django-hosting.ch"
        context["google_analytics"] = "UA-62285904-6"
        context["email"] = "info@django-hosting.ch"
        context["vm_types"] = VirtualMachineType.get_serialized_vm_types()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class RailsHostingView(View):
    template_name = "hosting/rails.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["hosting"] = "rails"
        context["hosting_long"] = "Ruby On Rails"
        context["domain"] = "rails-hosting.ch"
        context["google_analytics"] = "UA-62285904-5"
        context["email"] = "info@rails-hosting.ch"
        context["vm_types"] = VirtualMachineType.get_serialized_vm_types()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class NodeJSHostingView(View):
    template_name = "hosting/nodejs.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["hosting"] = "nodejs"
        context["hosting_long"] = "NodeJS"
        context["domain"] = "node-hosting.ch"
        context["google_analytics"] = "UA-62285904-7"
        context["email"] = "info@node-hosting.ch"
        context["vm_types"] = VirtualMachineType.get_serialized_vm_types()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class IndexView(View):
    template_name = "hosting/index.html"

    def get_context_data(self, **kwargs):
        context = {}
        context["hosting"] = "nodejs"
        context["hosting_long"] = "NodeJS"
        context["domain"] = "node-hosting.ch"
        context["google_analytics"] = "UA-62285904-7"
        context["email"] = "info@node-hosting.ch"
        context["vm_types"] = VirtualMachineType.get_serialized_vm_types()
        return context

    def get(self, request, *args, **kwargs):
        context = self.get_context_data()
        return render(request, self.template_name, context)


class LoginView(FormView):
    template_name = 'hosting/login.html'
    form_class = HostingUserLoginForm
    moodel = CustomUser
    success_url = reverse_lazy('hosting:login')

    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        auth_user = authenticate(email=email, password=password)
        if auth_user:
            login(self.request, auth_user)
            return HttpResponseRedirect(self.get_success_url())
        return HttpResponseRedirect(self.get_success_url())


class SignupView(CreateView):
    template_name = 'hosting/signup.html'
    form_class = HostingUserSignupForm
    moodel = CustomUser

    def get_success_url(self):
        return reverse_lazy('hosting:signup')

    def form_valid(self, form):
        name = form.cleaned_data.get('name')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        CustomUser.register(name, password, email)
        auth_user = authenticate(email=email, password=password)
        login(self.request, auth_user)
        return HttpResponseRedirect(self.get_success_url())



# class RailsBetaUserForm(ModelForm):
#     required_css_class = 'form-control'
#     class Meta:
#         model = RailsBetaUser
#         fields = [ 'email' ]

# def hosting(request, context):
#     email = RailsBetaUser(received_date=datetime.datetime.now())

#     if request.method == 'POST':
#         context['form'] = RailsBetaUserForm(request.POST, instance=email)
#         if context['form'].is_valid():
#             context['form'].save()
#             email = context['form'].cleaned_data['email']
#             subject = "%shosting request" % context['hosting']
#             message = "Request for beta by: %s" % email

#             mail_managers(subject, message)

#             return HttpResponseRedirect(reverse("hosting:beta"))
#         else:
#             context['form'] = RailsBetaUserForm()
#             context['error_message'] = "a problem"

#     page = "hosting/%s.html" % context['hosting']

#     return render(request, page, context)

# def beta(request):
#     return render(request, 'hosting/beta.html')

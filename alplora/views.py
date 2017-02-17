from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = "alplora/index.html"

class LoginView(TemplateView):
    template_name = "alplora/login.html"

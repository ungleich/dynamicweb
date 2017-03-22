from django.views.generic import TemplateView
from django.utils.translation import get_language

class IndexView(TemplateView):
    template_name = "alplora/index.html"
	
    def get_context_data(self, *args, **kwargs):
    	context = super(IndexView, self).get_context_data(**kwargs)
    	language = get_language()
    	context.update({
    		'language': language
    	})
    	return context


class LoginView(TemplateView):
    template_name = "alplora/login.html"

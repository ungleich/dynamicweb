from django.views.generic import TemplateView
from django.utils.translation import get_language, get_language_info

class IndexView(TemplateView):
	template_name = "alplora/index.html"

	def get_context_data(self, *args, **kwargs):
		context = super(IndexView, self).get_context_data(**kwargs)
		languages = getlanguages()
		context.update(languages)
		return context


class LoginView(TemplateView):
	template_name = "alplora/login.html"

	def get_context_data(self, *args, **kwargs):
		context = super(LoginView, self).get_context_data(**kwargs)
		languages = getlanguages()
		context.update(languages)
		return context


def getlanguages():
	language = get_language()
	language_activate = get_language_info(language)
	if language == 'de':
		list_language = {
			'name': 'English',
			'code': 'en-us'
		}
	else:
		list_language = {
			'name': 'Deutsch',
			'code': 'de'
		}

	return {
		'language': language,
		'list_language': list_language,
		'language_activate': language_activate['name_local']
	}

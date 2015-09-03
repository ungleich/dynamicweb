from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'beta$', views.beta, name='beta'),
    url(r'django$', views.djangohosting, name='djangohosting'), 
    url(r'nodejs$', views.nodejshosting, name='nodejshosting'),
    url(r'rails$', views.railshosting,   name='railshosting'),
]

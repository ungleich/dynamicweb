from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'beta$', views.beta, name='beta'),
    url(r'djangohosting$', views.djangohosting, name='djangohosting'), 
    url(r'nodejshosting$', views.nodejshosting, name='nodejshosting'),
    url(r'railshosting$', views.railshosting, name='railshosting'),
]

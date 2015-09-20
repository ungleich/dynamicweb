from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about$', views.about, name='about'),
    url(r'contact$', views.contact, name='contact'),
    url(r'letscowork$', views.letscowork, name='letscowork'),
    url(r'home$', views.home, name='home'),
]

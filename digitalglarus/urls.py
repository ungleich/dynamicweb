from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'_about$', views.about, name='about'),
    url(r'_contact$', views.contact, name='contact'),
    url(r'_letscowork$', views.letscowork, name='letscowork'),
    url(r'_home$', views.home, name='home'),
    url(r'blog/$', views.blog, name='blog'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
]

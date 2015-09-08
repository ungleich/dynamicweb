from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'about$', views.about, name='about'),
    url(r'contact$', views.contact, name='contact'),
    url(r'blog/$', views.blog, name='blog'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
]

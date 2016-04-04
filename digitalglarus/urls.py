from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'old_contact$', views.contact, name='contact'),
    url(r'supporters/$', views.supporters, name='supporters'),
    # url(r'', views.index, name='index'),
    url(r'blog/',views.blog,name='blog'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
]

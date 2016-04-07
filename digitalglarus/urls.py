from django.conf.urls import url

from . import views
from .views import ContactView

urlpatterns = [
    url(r'contact/?$', ContactView.as_view(), name='contact'),
    url(r'supporters/?$', views.supporters, name='supporters'),
    url(r'support-us/?$', views.support, name='support'),    # url(r'', views.index, name='index'),
    url(r'blog/',views.blog,name='blog'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
]

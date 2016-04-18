from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _
from . import views
from .views import ContactView

urlpatterns = [
    url(_(r'contact/?$'), ContactView.as_view(), name='contact'),
    url(_(r'supporters/?$'), views.supporters, name='supporters'),
    url(_(r'support-us/?$'), views.support, name='support'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
    url(r'blog/$', views.blog, name='blog'),
]

from django.conf.urls import url

from django.utils.translation import ugettext_lazy as _
from . import views
from .views import ContactView, IndexView, AboutView

urlpatterns = [
#    url(r'^$', IndexView.as_view(), name='home'),
   # url(_(r'home/?$'), IndexView.as_view(), name='home'),
   # url(_(r'about/?$'), AboutView.as_view(), name='about'),
    url(_(r'contact/?$'), ContactView.as_view(), name='contact'),
    url(_(r'supporters/?$'), views.supporters, name='supporters'),
    url(r'calendar_api/(?P<month>\d+)/(?P<year>\d+)?$',views.CalendarApi.as_view()),
    url(r'calendar_api/',views.CalendarApi.as_view()),
    url(_(r'support-us/?$'), views.support, name='support'),
    url(r'^blog/(?P<slug>\w[-\w]*)/$', views.blog_detail, name='blog-detail'),
    url(r'blog/$', views.blog, name='blog'),
]

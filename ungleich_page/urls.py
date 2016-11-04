from django.conf.urls import url
from . import views as up_views
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^$', up_views.LandingView.as_view(), name='landing'),
    # url(r'^ungleich_page/?$', LandingView.as_view(), name='landing'),
    url(_(r'contact/$'), up_views.ContactView.as_view(), name='contact'),
]

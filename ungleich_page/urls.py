from django.conf.urls import url
from .views import ContactView, LandingView
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'', LandingView.as_view(), name='landing'),
    url(_(r'contact/$'), ContactView.as_view(), name='contact'),
]

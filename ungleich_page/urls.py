from django.conf.urls import url
from .views import ContactView, LandingView, WhyUngleichView
from django.utils.translation import ugettext_lazy as _

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    # url(r'^ungleich_page/?$', LandingView.as_view(), name='landing'),
    url(_(r'contact/$'), ContactView.as_view(), name='contact'),
    #the url for whyUngleich
    url(_(r'whyungleich/$'), WhyUngleichView.as_view(), name='whyungleichs'),
]

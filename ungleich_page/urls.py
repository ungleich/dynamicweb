from django.conf.urls import url
from .views import ContactView
from django.utils.translation import ugettext_lazy as _


urlpatterns = [
    url(_(r'contact/?$'), ContactView.as_view(), name='contact'),
]

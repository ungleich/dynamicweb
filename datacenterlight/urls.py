from django.conf.urls import url
from django.views.generic import TemplateView, RedirectView

from .views import (
    IndexView, PaymentOrderView, OrderConfirmationView,
    WhyDataCenterLightView, ContactUsView
)


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^t/$', IndexView.as_view(), name='index_t'),
    url(r'^g/$', IndexView.as_view(), name='index_g'),
    url(r'^f/$', IndexView.as_view(), name='index_f'),
    url(r'^l/$', IndexView.as_view(), name='index_l'),
    url(r'^new/$', RedirectView.as_view(url='/cms/'),
        name='cms_index'),
    url(r'^whydatacenterlight/?$', WhyDataCenterLightView.as_view(),
        name='whydatacenterlight'),
    url(r'^payment/?$', PaymentOrderView.as_view(), name='payment'),
    url(r'^order-confirmation/?$', OrderConfirmationView.as_view(),
        name='order_confirmation'),
    url(r'^contact/?$', ContactUsView.as_view(), name='contact_us'),
    url(r'glasfaser/?$',
        TemplateView.as_view(template_name='ungleich_page/glasfaser.html'),
        name='glasfaser'),
]

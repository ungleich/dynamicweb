from django.conf.urls import url
from django.views.generic import TemplateView

from .views import IndexView, BetaProgramView, LandingProgramView, BetaAccessView, PricingView, SuccessView, \
    PaymentOrderView, OrderConfirmationView, WhyDataCenterLightView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^whydatacenterlight/?$', WhyDataCenterLightView.as_view(),
        name='whydatacenterlight'),
    url(r'^beta-program/?$', BetaProgramView.as_view(), name='beta'),
    url(r'^landing/?$', LandingProgramView.as_view(), name='landing'),
    url(r'^pricing/?$', PricingView.as_view(), name='pricing'),
    url(r'^payment/?$', PaymentOrderView.as_view(), name='payment'),
    url(r'^order-confirmation/?$', OrderConfirmationView.as_view(),
        name='order_confirmation'),
    url(r'^order-success/?$', SuccessView.as_view(), name='order_success'),
    url(r'^beta_access?$', BetaAccessView.as_view(), name='beta_access'),

    url(r'test/?$', TemplateView.as_view(template_name='datacenterlight/downtime.html')),
]

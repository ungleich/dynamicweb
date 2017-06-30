from django.conf.urls import url

from .views import IndexView, BetaProgramView, LandingProgramView, \
    BetaAccessView, PricingView, SuccessView, PaymentOrderView, OrderConfirmationView


urlpatterns = [
    url(r'^/?$', IndexView.as_view(), name='index'),
    url(r'^/beta-program/?$', BetaProgramView.as_view(), name='beta'),
    url(r'^/landing/?$', LandingProgramView.as_view(), name='landing'),
    url(r'^/pricing/?$', PricingView.as_view(), name='pricing'),
    url(r'^/payment/?$', PaymentOrderView.as_view(), name='payment'),
    url(r'^/order-confirmation/(?P<pk>\d+)/?$', OrderConfirmationView.as_view(), name='order_confirmation'),
    url(r'^/order-success/?$', SuccessView.as_view(), name='order_success'),
    url(r'^/beta_access?$', BetaAccessView.as_view(), name='beta_access'),
]

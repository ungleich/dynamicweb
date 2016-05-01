from django.conf.urls import url

from .views import DjangoHostingView, RailsHostingView, PaymentVMView, \
                    NodeJSHostingView, LoginView, SignupView, IndexView

urlpatterns = [
    # url(r'pricing/?$', VMPricingView.as_view(), name='pricing'),
    url(r'index/?$', IndexView.as_view(), name='index'),
    url(r'django/?$', DjangoHostingView.as_view(), name='djangohosting'),
    url(r'nodejs/?$', NodeJSHostingView.as_view(), name='nodejshosting'),
    url(r'rails/?$', RailsHostingView.as_view(),   name='railshosting'),
    url(r'login/?$', LoginView.as_view(),  name='login'),
    url(r'signup/?$', SignupView.as_view(), name='signup'),
    url(r'payment/?$', PaymentVMView.as_view(), name='payment'),
]

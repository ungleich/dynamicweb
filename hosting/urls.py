from django.conf.urls import url

from . import views
from .views import VMPricingView, DjangoHostingView

urlpatterns = [
    url(r'beta$', views.beta, name='beta'),
    url(r'pricing/?$', VMPricingView.as_view(), name='pricing'),
    url(r'django/?$', DjangoHostingView.as_view(), name='djangohosting'),
    url(r'nodejs$', views.nodejshosting, name='nodejshosting'),
    url(r'rails$', views.railshosting,   name='railshosting'),
]

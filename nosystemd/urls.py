from django.conf.urls import url

from .views import LandingView, LoginView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
]

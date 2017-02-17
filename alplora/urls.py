from django.conf.urls import url

from .views import IndexView


urlpatterns = [
    url(r'^/?$', IndexView.as_view(), name='index'),
#     url(r'^/beta-program/?$', BetaProgramView.as_view(), name='beta'),
#     url(r'^/landing/?$', LandingProgramView.as_view(), name='landing'),
]

from django.conf.urls import url

from .views import IndexView, LoginView, ContactView


urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'login/', LoginView.as_view(), name='login'),
    url(r'contact', ContactView.as_view(), name='contact'),
    #     url(r'^/beta-program/?$', BetaProgramView.as_view(), name='beta'),
    #     url(r'^/landing/?$', LandingProgramView.as_view(), name='landing'),
]

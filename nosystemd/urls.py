from django.conf.urls import url
from django.contrib.auth import views as auth_views

from .views import LandingView, LoginView, SignupView, PasswordResetView,\
    PasswordResetConfirmView, DonationView, DonationDetailView, ChangeDonatorStatusDetailView,\
    DonatorStatusDetailView, DonationListView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^signup/?$', SignupView.as_view(), name='signup'),
    url(r'^logout/?$', auth_views.logout,
        {'next_page': '/nosystemd/login?logged_out=true'}, name='logout'),
    url(r'reset-password/?$', PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^donations/?$', DonationListView.as_view(), name='donations'),
    url(r'donations/(?P<pk>\d+)/?$', DonationDetailView.as_view(), name='donations'),
    url(r'^make_donation/?$', DonationView.as_view(), name='make_donation'),
    url(r'donations/status/?$', DonatorStatusDetailView.as_view(),
        name='donator_status'),
    url(r'donations/status/(?P<pk>\d+)/?$', ChangeDonatorStatusDetailView.as_view(),
        name='change_donator_status'),
    # url(r'^donation/invoice?$', DonationView.as_view(), name='donation_detail'),

]

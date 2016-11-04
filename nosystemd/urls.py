from django.conf.urls import url
from django.contrib.auth import views as auth_views

from . import views as nosystemd_views

urlpatterns = [
    url(r'^$', nosystemd_views.LandingView.as_view(), name='landing'),
    url(r'^login/?$', nosystemd_views.LoginView.as_view(), name='login'),
    url(r'^signup/?$', nosystemd_views.SignupView.as_view(), name='signup'),
    url(r'^logout/?$', auth_views.logout,{'next_page':'/nosystemd/login?logged_out=true'}),
    url(r'reset-password/?$', nosystemd_views.PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        nosystemd_views.PasswordResetConfirmView.as_view(), name='reset_password_confirm'),
    url(r'^donations/?$', nosystemd_views.DonationListView.as_view(), name='donations'),
    url(r'donations/(?P<pk>\d+)/?$', nosystemd_views.DonationDetailView.as_view(), name='donations'),
    url(r'^make_donation/?$', nosystemd_views.DonationView.as_view(), name='make_donation'),
    url(r'donations/status/?$', nosystemd_views.DonatorStatusDetailView.as_view(),
        name='donator_status'),
    url(r'donations/status/(?P<pk>\d+)/?$', nosystemd_views.ChangeDonatorStatusDetailView.as_view(),
        name='change_donator_status'),
    # url(r'^donation/invoice?$', DonationView.as_view(), name='donation_detail'),

]

from django.conf.urls import url

from .views import LandingView, LoginView, SignupView, PasswordResetView,\
    PasswordResetConfirmView, DonationView

urlpatterns = [
    url(r'^$', LandingView.as_view(), name='landing'),
    url(r'^login/?$', LoginView.as_view(), name='login'),
    url(r'^signup/?$', SignupView.as_view(), name='signup'),
    url(r'^logout/?$', 'django.contrib.auth.views.logout',
        {'next_page': '/nosystemd/login?logged_out=true'}, name='logout'),
    url(r'reset-password/?$', PasswordResetView.as_view(), name='reset_password'),
    url(r'reset-password-confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$',
        PasswordResetConfirmView.as_view(), name='reset_password_confirm'),

    url(r'^donation/?$', DonationView.as_view(), name='donation'),

]

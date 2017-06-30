__author__ = 'tomislav'
from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = (
    url(r"^$", views.LoginRegistrationView.as_view(), name='login_glarus'),
    url(r"^validate/(?P<validate_slug>.*)/$", views.validate_email),
    url(r"^membership/$", login_required(views.MembershipView.as_view()), name='membership'),
    url(r'logout/?$', views.logout_glarus, name='logout_glarus'),
    url(r"^buy/(?P<time>\w+)/$", login_required(views.CreditCardView.as_view()), name='payment'),
    url(r'^buy/(?P<time>\w+)/reset', login_required(views.reset), name='reset')
)

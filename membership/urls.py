__author__ = 'tomislav'
from django.conf.urls import url

from . import views

urlpatterns = (
    url(r"^/$", views.LoginRegistrationView.as_view()),
    url(r"^/validate/(?P<validate_slug>.*)/$", views.validate_email),
    url(r"^/membership/$",views.MembershipView.as_view(),name='membership')
)

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'send_message', views.send_message, name='send_message'),
    url(r'^(?P<message_id>[0-9]+)/$', views.detail, name='detail'),
]

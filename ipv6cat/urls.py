from django.conf.urls import url
from .views import home, CatDetailView


urlpatterns = [
    url(r'^$', home, name='home'),
    url(r'^(?P<slug>[\w-]+)/$', CatDetailView.as_view(), name='detail'),
]

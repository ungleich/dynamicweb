from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$',views.PostListViewUngleich.as_view()),
    # url(r'^$',views.PostListView.as_view()),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',views.details)

]
from django.conf.urls import url
from . import views
from .views import PostDetailViewUngleich

urlpatterns = [
    url(r'^$', views.PostListViewUngleich.as_view(), name="post-list"),
    # url(r'^$',views.PostListView.as_view()),
    url(r'^(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',
        PostDetailViewUngleich.as_view(), name="post-detail")
]

from django.conf.urls import url, include
from rest_framework.urlpatterns import format_suffix_patterns
from .views import VmCreateView, VmDetailsView

urlpatterns = {
    url(r'^auth/', include('rest_framework.urls', namespace='rest_framework')),

    url(r'^vms/$', VmCreateView.as_view(), name="vm_create"),
    url(r'^vms/(?P<pk>[0-9]+)/$', VmDetailsView.as_view(),
        name="vm_details"),
}

urlpatterns = format_suffix_patterns(urlpatterns)

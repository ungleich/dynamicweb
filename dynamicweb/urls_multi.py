from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views import static as static_view

urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^multi/', include('cms.urls')),
)

urlpatterns += [
    url(r'^media/(?P<path>.*)$',
        static_view.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]

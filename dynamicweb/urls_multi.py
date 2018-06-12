from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.i18n import i18n_patterns
from django.contrib import admin
from django.views import static as static_view
from django.views.generic import RedirectView

urlpatterns = i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^cms/', include('cms.urls')),
    url(r'^$', RedirectView.as_view(url='/cms')),
)

urlpatterns += [
    url(r'^media/(?P<path>.*)$',
        static_view.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]

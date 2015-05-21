from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^digital.glarus/', include('digital_glarus.urls',
        namespace="digital_glarus")),
    url(r'^', include('cms.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

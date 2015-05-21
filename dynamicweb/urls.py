from django.conf.urls import include, url
from django.contrib import admin
# deprecated in version 1.8
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from dynamicweb import settings

urlpatterns = i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^digital.glarus/', include('digital_glarus.urls',
        namespace="digital_glarus")),
    url(r'^', include('cms.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

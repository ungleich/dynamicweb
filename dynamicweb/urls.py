from django.conf.urls import patterns, include, url
from django.contrib import admin
# deprecated in version 1.8
from django.conf.urls.static import static
# i18n
from django.conf.urls.i18n import i18n_patterns

from dynamicweb import settings

urlpatterns = [
    url(r'^digitalglarus/', include('digitalglarus.urls',
                                     namespace="digitalglarus")),
    url(r'^hosting/', include('hosting.urls', namespace="hosting")),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^jsi18n/(?P<packages>\S+?)/$', 'django.views.i18n.javascript_catalog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# note the django CMS URLs included via i18n_patterns
urlpatterns += i18n_patterns('',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve', {
                                    'document_root': settings.MEDIA_ROOT,
                                }),
                            )

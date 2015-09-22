from django.conf.urls import patterns, include, url
from django.contrib import admin
# deprecated in version 1.8
from django.conf.urls.static import static

from dynamicweb import settings
from hosting.views import railshosting

urlpatterns = [
    url(r'^digitalglarus/', include('digitalglarus.urls',
                                    namespace="digitalglarus")),
    url(r'^hosting/', include('hosting.urls', namespace="hosting")),
    url(r'^railshosting/', railshosting, name="rails.hosting"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^', include('cms.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^jsi18n/(?P<packages>\S+?)/$',
        'django.views.i18n.javascript_catalog'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve', {
                                    'document_root': settings.MEDIA_ROOT,
                                }),
                            )

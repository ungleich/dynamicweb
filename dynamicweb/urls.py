from django.conf.urls import patterns, include, url
from django.contrib import admin
# deprecated in version 1.8
from django.conf.urls.static import static
from dynamicweb import settings

urlpatterns = [
    url(r'^admin/', include(admin.site.urls)),
    url(r'^digitalglarus/', include('digitalglarus.urls',
                                     namespace="digitalglarus")),
    url(r'^railshosting/', include('railshosting.urls',
                                   namespace="railshosting")),
    url(r'^cms/', include('cms.urls')),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve', {
                                    'document_root': settings.MEDIA_ROOT,
                                }),
                            )

from django.conf.urls import patterns, include, url
from django.contrib import admin
# deprecated in version 1.8
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static

from django.conf import settings
from hosting.views import RailsHostingView, DjangoHostingView, NodeJSHostingView
from membership import urls as membership_urls
from ungleich_page.views import LandingView
import debug_toolbar

urlpatterns = [   url(r'^index.html$', LandingView.as_view()),
                  url(r'^hosting/', include('hosting.urls', namespace="hosting")),
                  url(r'^hosting/', include('hosting.urls', namespace="hosting")),
                  url(r'^railshosting/', RailsHostingView.as_view(), name="rails.hosting"),
                  url(r'^nodehosting/', NodeJSHostingView.as_view(), name="node.hosting"),
                  url(r'^djangohosting/', DjangoHostingView.as_view(), name="django.hosting"),
                  url(r'^nosystemd/', include('nosystemd.urls', namespace="nosystemd")),
                  url(r'^datacenterlight', include('datacenterlight.urls', namespace="datacenterlight")),
                  url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
                  url(r'^jsi18n/(?P<packages>\S+?)/$',
                      'django.views.i18n.javascript_catalog'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# note the django CMS URLs included via i18n_patterns
urlpatterns += i18n_patterns('',
                             url(r'^/?$', LandingView.as_view()),
                             url(r'^admin/', include(admin.site.urls)),
                             url(r'^bill/', include('bill.urls')),
                             url(r'^membership/', include(membership_urls)),
                             url(r'^digitalglarus/', include('digitalglarus.urls',
                                                             namespace="digitalglarus")),
                             #url(r'^blog/', include('ungleich.urls', namespace='ungleich')),
                             url(r'^',
                                 include('ungleich_page.urls', namespace='ungleich_page'),
                                 name='ungleich_page'),
                             url(r'^blog/', include('ungleich.urls', namespace='ungleich')),
                             url(r'^', include('cms.urls'))
                             )

if settings.DEBUG:
    urlpatterns += patterns('',
                            url(r'^media/(?P<path>.*)$',
                                'django.views.static.serve', {
                                    'document_root': settings.MEDIA_ROOT,
                                }),
                            )
    urlpatterns += patterns('',url(r'^__debug__/', include(debug_toolbar.urls)))

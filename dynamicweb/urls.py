from cms.models.pagemodel import Page
from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.sites.models import Site
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.views import i18n, static as static_view

from django.conf import settings
from hosting.views import (
    RailsHostingView, DjangoHostingView, NodeJSHostingView
)
from datacenterlight.views import PaymentOrderView
from membership import urls as membership_urls
from ungleich_page.views import LandingView
from django.views.generic import RedirectView
from django.core.urlresolvers import reverse_lazy
import debug_toolbar

urlpatterns = [
    url(r'^index.html$', LandingView.as_view()),
    url(r'^open_api/',
        include('opennebula_api.urls', namespace='opennebula_api')),
    url(r'^railshosting/', RailsHostingView.as_view(),
        name="rails.hosting"),
    url(r'^nodehosting/', NodeJSHostingView.as_view(),
        name="node.hosting"),
    url(r'^djangohosting/', DjangoHostingView.as_view(),
        name="django.hosting"),
    url(r'^nosystemd/', include('nosystemd.urls', namespace="nosystemd")),
    url(r'^taggit_autosuggest/', include('taggit_autosuggest.urls')),
    url(r'^jsi18n/(?P<packages>\S+?)/$', i18n.javascript_catalog),
    url(r'^product/(?P<product_slug>[\w-]+)/$',
        PaymentOrderView.as_view(),
        name='show_product'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += i18n_patterns(
    url(r'^hosting/', include('hosting.urls', namespace="hosting")),
)

# note the django CMS URLs included via i18n_patterns
REDIRECT_TO_CMS = False
if Page.objects.filter(site_id=Site.objects.get_current().id).count():
    REDIRECT_TO_CMS = True

urlpatterns += i18n_patterns(
    url(r'^admin/', include(admin.site.urls)),
    url(r'^datacenterlight/',
        include('datacenterlight.urls', namespace="datacenterlight")),
    url(r'^hosting/', RedirectView.as_view(url=reverse_lazy('hosting:login')),
        name='redirect_hosting_login'),
    url(r'^alplora/', include('alplora.urls', namespace="alplora")),
    url(r'^membership/', include(membership_urls)),
    url(r'^digitalglarus/',
        include('digitalglarus.urls', namespace="digitalglarus")),
    url(r'^cms/blog/', include('ungleich.urls', namespace='ungleich')),
    url(r'^blog/(?P<year>\d{4})/(?P<month>\d{1,2})/(?P<day>\d{1,2})/(?P<slug>\w[-\w]*)/$',
        RedirectView.as_view(pattern_name='ungleich:post-detail')),
    url(r'^blog/$',
        RedirectView.as_view(url=reverse_lazy('ungleich:post-list')),
        name='blog_list_view'),
    url(r'^cms/', include('cms.urls')),
    url(r'^blog/', include('djangocms_blog.urls', namespace='djangocms_blog')),
    url(r'^$', RedirectView.as_view(url='/cms') if REDIRECT_TO_CMS
        else LandingView.as_view()),
    url(r'^', include('ungleich_page.urls', namespace='ungleich_page')),
)

urlpatterns += [
    url(r'^media/(?P<path>.*)$',
        static_view.serve, {
            'document_root': settings.MEDIA_ROOT,
        }),
]

if settings.DEBUG:
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls))]

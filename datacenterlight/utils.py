from django.contrib.sites.models import Site

from .cms_models import CMSIntegration


def get_cms_integration(name):
    current_site = Site.objects.get_current()
    try:
        cms_integration = CMSIntegration.objects.get(
            name=name, domain=current_site
        )
    except CMSIntegration.DoesNotExist:
        cms_integration = CMSIntegration.objects.get(name=name, domain=None)
    return cms_integration

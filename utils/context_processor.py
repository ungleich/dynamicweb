from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.

    Also check whether the site is a tenant site and create a corresponding
    variable to indicate this
    """
    host = request.get_host()
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_IDS', False).get(
        host)
    which_urlspy = settings.MULTISITE_CMS_URLS.get(host)
    if ga_prop_id is None:
        # Try checking if we have a www in host, if yes we remove
        # that and check in the dict again
        if host.startswith('www.'):
            ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_IDS',
                                 False).get(host[4:])
            which_urlspy = settings.MULTISITE_CMS_URLS.get(host[4:])
    return_dict = {}
    if not settings.DEBUG and ga_prop_id:
        return_dict['GOOGLE_ANALYTICS_PROPERTY_ID'] = ga_prop_id

    if which_urlspy:
        if which_urlspy.endswith("multi"):
            return_dict['IS_TENANT_SITE'] = True

    return return_dict

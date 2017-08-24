from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    host = request.get_host()
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_IDS', False).get(
        host)
    if ga_prop_id is None:
        # Try checking if we have a www in host, if yes we remove
        # that and check in the dict again
        if host.startswith('www.'):
            ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_IDS',
                                 False).get(host[4:])
    if not settings.DEBUG and ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id
        }
    return {}

from django.conf import settings


def google_analytics(request):
    """
    Use the variables returned in this function to
    render your Google Analytics tracking code template.
    """
    host = request.get_host()
    ga_prop_id = getattr(settings, 'GOOGLE_ANALYTICS_PROPERTY_IDS', False).get(host)
    print(ga_prop_id)
    if ga_prop_id:
        return {
            'GOOGLE_ANALYTICS_PROPERTY_ID': ga_prop_id
        }
    return {}
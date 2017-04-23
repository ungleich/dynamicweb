from .base import *
REGISTRATION_MESSAGE['message'] = REGISTRATION_MESSAGE['message'].format(host='dynamicweb-development.ungleich.ch',slug='{slug}')
ALLOWED_HOSTS = [
    "*"
    ]

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'unique-snowflake'
    }
}

MIDDLEWARE_CLASSES+=("debug_toolbar.middleware.DebugToolbarMiddleware",)

INSTALLED_APPS+=(
    'django_extensions',
    'debug_toolbar'
    )


#############################################
# configurations for opennebula-integration #
#############################################

# The user name of the OpenNebula infrastructure
OPENNEBULA_USERNAME = 'oneadmin'

# The password of the OpenNebula infrastructure
# The default credentials of the Sandbox OpenNebula VM is 
# oneadmin:opennebula
OPENNEBULA_PASSWORD = 'opennebula'

# The protocol is generally http or https
OPENNEBULA_PROTOCOL = 'http'

# The ip address or the domain name of the opennebula infrastructure
# OPENNEBULA_DOMAIN = '192.168.182.173'
# OPENNEBULA_DOMAIN = '192.168.122.225'
#OPENNEBULA_DOMAIN = '192.168.182.176'
OPENNEBULA_DOMAIN = '192.168.42.35'

# The port to connect in order to send an xmlrpc request. The default 
# port is 2633
OPENNEBULA_PORT = '2633'

# The endpoint to which the XML RPC request needs to be sent to. The 
# default value is /RPC2
OPENNEBULA_ENDPOINT = '/RPC2'

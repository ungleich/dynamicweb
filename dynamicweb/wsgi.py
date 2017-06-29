"""
WSGI config for dynamicweb project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os
import sys
from django.core.wsgi import get_wsgi_application

# sys.path.append(os.path.dirname(__file__))
sys.path.append('/home/app/pyvenv/lib/python3.4/site-packages/')

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "dynamicweb.settings.prod")

application = get_wsgi_application()

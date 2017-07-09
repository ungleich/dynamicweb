"""
Copyright 2015 ungleich.
"""

# -*- coding: utf-8 -*-
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os

from django.utils.translation import ugettext_lazy as _

# dotenv
import dotenv


def gettext(s):
    return s


def env(env_name):
    return os.environ.get(env_name)


def bool_env(val):
    """Replaces string based environment values with Python booleans"""
    return True if os.environ.get(val, False) == 'True' else False


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROJECT_DIR = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "../.."),
)

# load .env file
dotenv.read_dotenv("{0}/.env".format(PROJECT_DIR))

SITE_ID = 1

APP_ROOT_ENDPOINT = "/"
APPEND_SLASH = True

LOGIN_URL = None
LOGOUT_URL = None
LOGIN_REDIRECT_URL = None

EMAIL_HOST = "localhost"
EMAIL_PORT = 25
SECRET_KEY = env('DJANGO_SECRET_KEY')

# Application definition

INSTALLED_APPS = (
    # 1st migrate
    'membership',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'easy_thumbnails',
    'utils',
    'stored_messages',
    'mptt',
    'parler',
    'guardian',
    'taggit',
    'taggit_autosuggest',
    # 'django_select2',
    'meta',
    'meta_mixin',
    'bootstrap3',
    'compressor',
    'filer',
    'djangocms_blog',
    'cms',  # django CMS itself
    'aldryn_apphooks_config',
    'aldryn_boilerplates',
    'aldryn_categories',
    'aldryn_common',
    'aldryn_newsblog',
    'aldryn_people',
    'aldryn_reversion',
    'aldryn_translation_tools',
    'treebeard',  # utilities for implementing a tree
    'sekizai',  # for javascript and css management
    'menus',  # helper for model independent hierarchical website navigation
    'cmsplugin_filer_image',

    # 2nd migrate
    # django-cms plugins
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    # 'djangocms_flash',
    # 'djangocms_googlemap',
    # 'djangocms_inherit',
    # 'djangocms_link',
    # 'djangocms_teaser',
    'djangocms_page_meta',
    'djangocms_text_ckeditor',
    'djangocms_admin_style',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    # 'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    #
    # blog
    # versioning
    'reversion',
    # ungleich
    'ungleich',
    'ungleich_page',
    'hosting',
    'digitalglarus',
    'nosystemd',
    'datacenterlight',
    'datacenterlight.templatetags',
    'alplora',
    'rest_framework',
    'opennebula_api'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'utils.middleware.MultipleProxyMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    # django-cms middlewares
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'dynamicweb.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(PROJECT_DIR, 'cms_templates/'),
                 os.path.join(PROJECT_DIR, 'cms_templates/djangocms_blog/'),
                 os.path.join(PROJECT_DIR, 'membership'),
                 os.path.join(PROJECT_DIR, 'hosting/templates/'),
                 os.path.join(PROJECT_DIR, 'nosystemd/templates/'),
                 os.path.join(PROJECT_DIR, 'ungleich/templates/djangocms_blog/'),
                 os.path.join(PROJECT_DIR, 'ungleich/templates/cms/ungleichch'),
                 os.path.join(PROJECT_DIR, 'ungleich/templates/ungleich'),
                 os.path.join(PROJECT_DIR, 'ungleich_page/templates/ungleich_page'),
                 os.path.join(PROJECT_DIR, 'templates/analytics'),
                 ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                "django.core.context_processors.media",
                "django.core.context_processors.static",
                "django.core.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',
                'utils.context_processor.google_analytics',
            ],
        },
    },
]

WSGI_APPLICATION = 'dynamicweb.wsgi.application'

CMS_TEMPLATES = (
    ('base_glarus.html', gettext('default')),
    ('one_column.html', gettext('2 Column')),
    ('two_columns.html', gettext('3 Column')),
    ('about.html', gettext('DG.About')),
    ('contact.html', gettext('DG.Contact')),
    ('home_digitalglarus.html', gettext('DG.Home')),
    ('letscowork.html', gettext('DG.CoWork')),
    # ('detail.html', gettext('DG.Detail')),
    ('one_column.html', gettext('DG.OneColumn')),
    # ungleich
    ('blog_ungleich.html', gettext('Blog')),
    ('page.html', gettext('Page')),
)

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'app'
    }
}


AUTHENTICATION_BACKENDS = (
    'guardian.backends.ObjectPermissionBackend',
    'django.contrib.auth.backends.ModelBackend',
)


# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True

LANGUAGES = (
    ('en-us', _('English')),
    ('de', _('Deutsch')),
)

LANGUAGE_CODE = 'en-us'

LOCALE_PATHS = [

    os.path.join(PROJECT_DIR, 'digitalglarus/locale'),
]

CMS_PLACEHOLDER_CONF = {
    'logo_image': {
        'name': 'Logo Image',
        'plugins': ['FilerImagePlugin'],
        'limits': {
            'global': 1,
        }
    },
    'page-title': {
        'name': 'Page Title',
        'plugins': ['TextPlugin'],
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body': 'Page Title...'
                }
            }
        ],
        'limits': {
            'global': 1,
        }
    },
    'page-subtitle': {
        'name': 'Page Subtitle',
        'inherit': 'page-title',
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body': 'Page subtitle...'
                }
            }
        ],
    },
    'footer_copyright': {
        'name': 'Copyright',
        'inherit': 'page-title',
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {
                    'body': 'Copyright...'
                }
            }
        ],
    },
    'content': {
        'name': _('Content'),
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {'body': '<p></p>'},
            },
        ]
    },
    'post_content': {
        'name': _('Content'),
        'default_plugins': [
            {
                'plugin_type': 'TextPlugin',
                'values': {'body': '<p></p>'},
            },
        ]
    },
}

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.PyLibMCCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

if LOGIN_URL is None:
    LOGIN_URL = APP_ROOT_ENDPOINT + 'login/'
if LOGOUT_URL is None:
    LOGOUT_URL = APP_ROOT_ENDPOINT + 'logout/'
if LOGIN_REDIRECT_URL is None:
    LOGIN_REDIRECT_URL = APP_ROOT_ENDPOINT

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
MEDIA_URL = APP_ROOT_ENDPOINT + 'media/'
FILE_UPLOAD_PERMISSIONS = 0o644

META_SITE_PROTOCOL = 'http'
META_USE_SITES = True
MIGRATION_MODULES = {
    'cms': 'cms.migrations',
    # 'filer': 'filer.migrations_django',
    # 'menus': 'menus.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_link': 'djangocms_link.migrations_django',
    'djangocms_teaser': 'djangocms_teaser.migrations_django',
    'djangocms_column': 'djangocms_column.migrations_django',
    'djangocms_flash': 'djangocms_flash.migrations_django',
    'djangocms_googlemap': 'djangocms_googlemap.migrations_django',
    'djangocms_inherit': 'djangocms_inherit.migrations_django',
    'djangocms_style': 'djangocms_style.migrations_django',
    'cmsplugin_filer_image': 'cmsplugin_filer_image.migrations_django',
    'cmsplugin_filer_file': 'cmsplugin_filer_file.migrations_django',
    'cmsplugin_filer_folder': 'cmsplugin_filer_folder.migrations_django',
    'cmsplugin_filer_link': 'cmsplugin_filer_link.migrations_django',
    'cmsplugin_filer_teaser': 'cmsplugin_filer_teaser.migrations_django',
    'cmsplugin_filer_utils': 'cmsplugin_filer_utils.migrations_django',
    'cmsplugin_filer_video': 'cmsplugin_filer_video.migrations_django',
    'djangocms_text_ckeditor': 'djangocms_text_ckeditor.migrations',
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

# COMPRESS_PRECOMPILERS = (
#    ('text/less', 'lesscpy {infile}'),
# )

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)

# django-cms-text-ckeditor
TEXT_SAVE_IMAGE_FUNCTION = (
    'cmsplugin_filer_image.integrations.ckeditor.create_image_plugin'
)
TEXT_ADDITIONAL_TAGS = ('iframe',)
TEXT_ADDITIONAL_ATTRIBUTES = ('scrolling', 'allowfullscreen', 'frameborder')
USE_X_FORWARDED_HOST = True

# Django Bootstrap - Settings
# Added Configuration for bootstrap static files to load over https.
BOOTSTRAP3 = {

    # The URL to the jQuery JavaScript file
    'jquery_url': '//code.jquery.com/jquery.min.js',

    # The Bootstrap base URL
    'base_url': '//maxcdn.bootstrapcdn.com/bootstrap/3.3.4/',

    # The complete URL to the Bootstrap CSS file
    # (None means derive it from base_url)
    'css_url': None,

    # The complete URL to the Bootstrap CSS file (None means no theme)
    'theme_url': None,

    # The complete URL to the Bootstrap JavaScript file
    # (None means derive it from base_url)
    'javascript_url': None,

    # Put JavaScript in the HEAD section of the HTML document
    # (only relevant if you use bootstrap3.html)
    'javascript_in_head': False,

    # Include jQuery with Bootstrap JavaScript
    # (affects django-bootstrap3 template tags)
    'include_jquery': False,

    # Label class to use in horizontal forms
    'horizontal_label_class': 'col-md-3',

    # Field class to use in horizontal forms
    'horizontal_field_class': 'col-md-9',

    # Set HTML required attribute on required fields
    'set_required': True,

    # Set HTML disabled attribute on disabled fields
    'set_disabled': False,

    # Set placeholder attributes to label if no placeholder is provided
    'set_placeholder': True,

    # Class to indicate required (better to set this in your Django form)
    'required_css_class': '',

    # Class to indicate error (better to set this in your Django form)
    'error_css_class': 'has-error',

    # Class to indicate success, meaning the field has valid input
    # (better to set this in your Django form)
    'success_css_class': 'has-success',

    # Renderers (only set these if you have studied the source and understand
    # the inner workings)
    'formset_renderers': {
        'default': 'bootstrap3.renderers.FormsetRenderer',
    },
    'form_renderers': {
        'default': 'bootstrap3.renderers.FormRenderer',
    },
    'field_renderers': {
        'default': 'bootstrap3.renderers.FieldRenderer',
        'inline': 'bootstrap3.renderers.InlineFieldRenderer',
    },
}

# djangocms_blog config

BLOG_ENABLE_COMMENTS = False
BLOG_USE_PLACEHOLDER = True
BLOG_IMAGE_THUMBNAIL_SIZE = {'size': '120x120', 'crop': True, 'upscale': False}
BLOG_IMAGE_FULL_SIZE = {'size': '640x120', 'crop': True, 'upscale': False}
BLOG_PAGINATION = 4
BLOG_LATEST_POSTS = BLOG_PAGINATION
BLOG_POSTS_LIST_TRUNCWORDS_COUNT = 100
BLOG_MULTISITE = True
BLOG_AUTHOR_DEFAULT = True

# django-meta
META_SITE_PROTOCOL = "https"
META_SITE_DOMAIN = "ungleich.ch"
META_SITE_TYPE = "website"
META_SITE_NAME = "ungleich"
META_INCLUDE_KEYWORDS = ["ungleich", "hosting", "switzerland",
                         "Schweiz", "Swiss", "cdist"]
META_USE_SITES = True

PARLER_LANGUAGES = {1: ({'code': 'en-us'}, {'code': 'de'},)}
AUTH_USER_MODEL = 'membership.CustomUser'


# PAYMENT

STRIPE_DESCRIPTION_ON_PAYMENT = "Payment for ungleich GmbH services"

# EMAIL MESSAGES
REGISTRATION_MESSAGE = {'subject': "Validation mail",
                        'message': 'Thank You for registering for account on Digital Glarus.\n'
                                   'Please verify Your account under following link '
                                   'http://{host}/en-us/digitalglarus/login/validate/{slug}',
                        }
STRIPE_API_PRIVATE_KEY = env('STRIPE_API_PRIVATE_KEY')
STRIPE_API_PUBLIC_KEY = env('STRIPE_API_PUBLIC_KEY')

ANONYMOUS_USER_NAME = 'anonymous@ungleich.ch'
GUARDIAN_GET_INIT_ANONYMOUS_USER = 'membership.models.get_anonymous_user_instance'


#############################################
# configurations for opennebula-integration #
#############################################

# The oneadmin user name of the OpenNebula infrastructure
OPENNEBULA_USERNAME = env('OPENNEBULA_USERNAME')

# The oneadmin password of the OpenNebula infrastructure
# The default credentials of the Sandbox OpenNebula VM is
# oneadmin:opennebula
OPENNEBULA_PASSWORD = env('OPENNEBULA_PASSWORD')

# The protocol is generally http or https
OPENNEBULA_PROTOCOL = env('OPENNEBULA_PROTOCOL')

# The ip address or the domain name of the opennebula infrastructure
OPENNEBULA_DOMAIN = env('OPENNEBULA_DOMAIN')

# The port to connect in order to send an xmlrpc request. The default
# port is 2633
OPENNEBULA_PORT = env('OPENNEBULA_PORT')

# The endpoint to which the XML RPC request needs to be sent to. The
# default value is /RPC2
OPENNEBULA_ENDPOINT = env('OPENNEBULA_ENDPOINT')


# dcl email configurations
DCL_TEXT = env('DCL_TEXT')
DCL_SUPPORT_FROM_ADDRESS = env('DCL_SUPPORT_FROM_ADDRESS')

# Settings for Google analytics
GOOGLE_ANALYTICS_PROPERTY_IDS = {
    'datacenterlight.ch': 'UA-62285904-9',
    'digitalglarus.ch': 'UA-62285904-2',
    '127.0.0.1:8000': 'localhost',
    'dynamicweb-development.ungleich.ch': 'development',
    'dynamicweb-staging.ungleich.ch': 'staging'
}

DEBUG = bool_env('DEBUG')

if DEBUG:
    from .local import * # flake8: noqa
else:
    from .prod import * # flake8: noqa

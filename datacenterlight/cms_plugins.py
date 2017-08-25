from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool
# from cms.plugins.text.models import Text @django-cms 2.x
from djangocms_text_ckeditor.models import Text  # djangocms 3.x
from djangocms_snippet.models import Snippet
from djangocms_snippet.cms_plugins import SnippetPlugin as SnippetPluginCMS
from djangocms_text_ckeditor.cms_plugins import TextPlugin as TextPluginCMS
from django.utils.translation import ugettext_lazy as _

# To have the editor free from all plugins, just a html editor
class TextPlugin(CMSPluginBase):
    model = Text
    name = _("Text HTML")
    render_template = "datacenterlight/text-html.html"

"""
Purpose of the below code is to have all the existent text plugins not to use any editor by default
but still able to use the editor with EditorTextPlugin
"""
plugin_pool.unregister_plugin(TextPluginCMS)  # unregisters the current TextPluginCMS
plugin_pool.register_plugin(TextPlugin)  # registers another TextPlugin that inherits from TextPluginCMS


class EditorTextPlugin(TextPluginCMS):
    name = _("Editor Text Plugin")


plugin_pool.register_plugin(EditorTextPlugin)

"""
Configure the CMS_PLACEHOLDER_CONF to use which plugins

CMS_PLACEHOLDER_CONF = {
    'content': {
        'plugin': {'TextPlugin', 'EditorTextPlugin'}
    }
}

Setting up the text.html
load i18n tag
Need to add {{instance.body|safe}}
"""

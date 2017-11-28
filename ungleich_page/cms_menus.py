from menus.base import NavigationNode
from menus.menu_pool import menu_pool
from django.utils.translation import ugettext_lazy as _
from cms.menu_bases import CMSAttachMenu
from cms.templatetags.cms_tags import _get_placeholder
from cms.utils.plugins import get_plugins


class GlasfaserMenu(CMSAttachMenu):

    name = _("Glasfaser menu")

    def get_nodes(self, request):
        nodes = []
        glasfaser_cms = 'ungleich_page/glasfaser_cms_page.html'
        if (request and request.current_page and
                request.current_page.get_template() == glasfaser_cms):
            template_context = {
                "request": request,
            }
            placeholder_name_list = [
                'Top Section', 'Middle Section',  'Glasfaser Services',
                'Glasfaser About', 'Contact Section'
            ]
            plugins_list = [
                'SectionWithImage', 'UngelichContactUsSection',
                'UngelichTextSection', 'Service', 'About'
            ]
            for placeholder_name in placeholder_name_list:
                placeholder = _get_placeholder(
                    request.current_page, request.current_page,
                    template_context, placeholder_name
                )
                plugins = get_plugins(
                    request, placeholder, request.current_page.get_template()
                )
                for plugin in plugins:
                    if type(plugin).__name__ in plugins_list:
                        section_hash = request.build_absolute_uri()
                        if hasattr(plugin, 'menu_text'):
                            menu_text = plugin.menu_text
                            if menu_text.strip() == '':
                                continue
                            menu_words = menu_text.split()
                            if len(menu_words) > 0:
                                section_hash = '{}#{}'.format(
                                    section_hash,
                                    menu_words[0]
                                )
                        else:
                            continue
                        newnode = NavigationNode(
                            menu_text,
                            url=section_hash,
                            id="{}-{}".format(
                                request.current_page.id, plugin.id
                            )
                        )
                        nodes.append(newnode)
        return nodes


menu_pool.register_menu(GlasfaserMenu)

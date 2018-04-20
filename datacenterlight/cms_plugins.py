from cms.plugin_base import CMSPluginBase
from cms.plugin_pool import plugin_pool

from .cms_models import (
    DCLBannerItemPluginModel, DCLBannerListPluginModel, DCLContactPluginModel,
    DCLFooterPluginModel, DCLLinkPluginModel, DCLNavbarDropdownPluginModel,
    DCLSectionIconPluginModel, DCLSectionImagePluginModel,
    DCLSectionPluginModel, DCLNavbarPluginModel,
    DCLSectionPromoPluginModel, DCLCustomPricingModel
)
from .models import VMTemplate, VMPricing


@plugin_pool.register_plugin
class DCLSectionPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Plugin"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/section.html"
    cache = False
    allow_children = True
    child_classes = [
        'DCLSectionIconPlugin', 'DCLSectionImagePlugin',
        'DCLSectionPromoPlugin', 'UngleichHTMLPlugin'
    ]

    def render(self, context, instance, placeholder):
        context = super(DCLSectionPlugin, self).render(
            context, instance, placeholder
        )
        context['children_to_side'] = []
        context['children_to_content'] = []
        if instance.child_plugin_instances is not None:
            right_children = [
                'DCLSectionImagePluginModel',
                'DCLSectionIconPluginModel'
            ]
            for child in instance.child_plugin_instances:
                if child.__class__.__name__ in right_children:
                    context['children_to_side'].append(child)
                else:
                    context['children_to_content'].append(child)
        return context


@plugin_pool.register_plugin
class DCLSectionIconPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Icon Plugin"
    model = DCLSectionIconPluginModel
    render_template = "datacenterlight/cms/section_icon.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLSectionImagePlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Image Plugin"
    model = DCLSectionImagePluginModel
    render_template = "datacenterlight/cms/section_image.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLSectionPromoPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Section Promo Plugin"
    model = DCLSectionPromoPluginModel
    render_template = "datacenterlight/cms/section_promo.html"
    cache = False


@plugin_pool.register_plugin
class DCLCalculatorPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Calculator Section Plugin"
    model = DCLSectionPluginModel
    render_template = "datacenterlight/cms/calculator.html"
    cache = False
    allow_children = True
    child_classes = [
        'DCLSectionPromoPlugin', 'UngleichHTMLPlugin', 'DCLCustomPricingPlugin'
    ]

    def render(self, context, instance, placeholder):
        context = super(DCLCalculatorPlugin, self).render(
            context, instance, placeholder
        )
        context['templates'] = VMTemplate.objects.all()
        context['children_to_content'] = []
        pricing_plugin_model = None
        if instance.child_plugin_instances is not None:
            context['children_to_content'].extend(
                instance.child_plugin_instances
            )
            for child in instance.child_plugin_instances:
                if child.__class__.__name__ == 'DCLCustomPricingModel':
                    # The second clause is just to make sure we pick up the
                    # most recent CustomPricing, if more than one is present
                    if (pricing_plugin_model is None or child.pricing_id >
                            pricing_plugin_model.model.pricing_id):
                        pricing_plugin_model = child

        if pricing_plugin_model:
            context['vm_pricing'] = VMPricing.get_vm_pricing_by_name(
                name=pricing_plugin_model.pricing.name
            )
        else:
            context['vm_pricing'] = VMPricing.get_default_pricing()

        return context


@plugin_pool.register_plugin
class DCLCustomPricingPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Custom Pricing Plugin"
    model = DCLCustomPricingModel
    render_plugin = False


@plugin_pool.register_plugin
class DCLBannerListPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Banner List Plugin"
    model = DCLBannerListPluginModel
    render_template = "datacenterlight/cms/banner_list.html"
    cache = False
    allow_children = True
    child_classes = ['DCLBannerItemPlugin']


@plugin_pool.register_plugin
class DCLBannerItemPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Banner Item Plugin"
    model = DCLBannerItemPluginModel
    render_template = "datacenterlight/cms/banner_item.html"
    cache = False
    require_parent = True
    parent_classes = ['DCLBannerListPlugin']


@plugin_pool.register_plugin
class DCLNavbarPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Navbar Plugin"
    model = DCLNavbarPluginModel
    render_template = "datacenterlight/cms/navbar.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin', 'DCLNavbarDropdownPlugin']


@plugin_pool.register_plugin
class DCLNavbarDropdownPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Navbar Dropdown Plugin"
    model = DCLNavbarDropdownPluginModel
    render_template = "datacenterlight/cms/navbar_dropdown.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']
    require_parent = True
    parent_classes = ['DCLNavbarPlugin']


@plugin_pool.register_plugin
class DCLLinkPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Link Plugin"
    model = DCLLinkPluginModel
    render_template = "datacenterlight/cms/link.html"
    cache = False
    require_parent = True


@plugin_pool.register_plugin
class DCLContactPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Contact Plugin"
    model = DCLContactPluginModel
    render_template = "datacenterlight/cms/contact.html"
    cache = False


@plugin_pool.register_plugin
class DCLFooterPlugin(CMSPluginBase):
    module = "Datacenterlight"
    name = "DCL Footer Plugin"
    model = DCLFooterPluginModel
    render_template = "datacenterlight/cms/footer.html"
    cache = False
    allow_children = True
    child_classes = ['DCLLinkPlugin']

from cms.extensions import PageExtension
from cms.extensions.extension_pool import extension_pool
from cms.models.fields import PlaceholderField
from cms.models.pluginmodel import CMSPlugin
from django import forms
from django.conf import settings
from django.contrib.postgres.fields import ArrayField
from django.contrib.sites.models import Site
from django.db import models
from django.utils.safestring import mark_safe
from djangocms_text_ckeditor.fields import HTMLField
from filer.fields.file import FilerFileField
from filer.fields.image import FilerImageField

from datacenterlight.models import VMPricing, VMTemplate


class CMSIntegration(models.Model):
    name = models.CharField(
        max_length=100, default='default',
        help_text=(
            'A unique name for the Integration. This name will be used to '
            'fetch the Integration into pages'
        )
    )
    footer_placeholder = PlaceholderField(
        'datacenterlight_footer', related_name='dcl-footer-placeholder+'
    )
    navbar_placeholder = PlaceholderField(
        'datacenterlight_navbar', related_name='dcl-navbar-placeholder+'
    )
    calculator_placeholder = PlaceholderField(
        'datacenterlight_calculator',
        related_name='dcl-calculator-placeholder+'
    )
    domain = models.ForeignKey(Site, null=True, blank=True)

    class Meta:
        unique_together = ('name', 'domain')

    def __str__(self):
        return self.name


class CMSFaviconExtension(PageExtension):
    favicon = FilerFileField(related_name="cms_favicon_image")


extension_pool.register(CMSFaviconExtension)


# Models for CMS Plugins

class DCLSectionPluginModel(CMSPlugin):
    heading = models.CharField(
        blank=True, null=True, max_length=100,
        help_text='An optional heading for the Section',
    )
    content = HTMLField()
    TEXT_DIRECTIONS = (
        ('left', 'Left'),
        ('right', 'Right')
    )
    text_direction = models.CharField(
        choices=TEXT_DIRECTIONS, max_length=10, default=True,
        help_text='The alignment of text in the section'
    )
    html_id = models.SlugField(
        blank=True, null=True,
        help_text=(
            'An optional html id for the Section. Required to set as target '
            'of a link on page'
        )
    )
    plain_heading = models.BooleanField(
        default=False,
        help_text='Select to keep the heading style simpler.'
    )
    center_on_mobile = models.BooleanField(
        default=False,
        help_text='Select to center align content on small screens.'
    )
    background_gradient = models.BooleanField(
        default=False,
        help_text='Select to add a gradient background to the section.'
    )

    def get_extra_classes(self):
        extra_classes = self.text_direction
        if self.center_on_mobile:
            extra_classes += ' section-sm-center'
        if self.background_gradient:
            extra_classes += ' section-gradient'
        if self.plain_heading:
            extra_classes += ' split-section-plain'
        return extra_classes

    def __str__(self):
        return '#' + self.html_id if self.html_id else str(self.pk)


class DCLBannerListPluginModel(CMSPlugin):
    heading = models.CharField(
        blank=True, null=True, max_length=100,
        help_text='An optional heading for the Section',
    )
    html_id = models.SlugField(
        blank=True, null=True,
        help_text=(
            'An optional html id for the Section. Required to set as target '
            'of a link on page'
        )
    )

    def __str__(self):
        return '#' + self.html_id if self.html_id else str(self.pk)


class DCLBannerItemPluginModel(CMSPlugin):
    content = HTMLField()
    banner_text = HTMLField(
        blank=True, null=True, max_length=100,
        help_text='Optional text to be shown as banner in other half.',
    )
    banner_image = FilerImageField(
        on_delete=models.CASCADE, null=True, blank=True,
        help_text='Optional image to be used in the banner in other half.'
    )
    TEXT_DIRECTIONS = (
        ('left', 'Left'),
        ('right', 'Right')
    )
    text_direction = models.CharField(
        choices=TEXT_DIRECTIONS, max_length=10, default=True,
        help_text='The alignment of text in the section'
    )

    def get_extra_classes(self):
        extra_classes = ''
        if self.text_direction == 'left':
            extra_classes = 'flex-row-rev'
        return extra_classes


class DCLLinkPluginModel(CMSPlugin):
    target = models.CharField(
        max_length=100,
        help_text='Url or #id to navigate to'
    )
    text = models.CharField(
        max_length=50,
        help_text='Text for the menu item'
    )
    title = models.CharField(
        blank=True, null=True, max_length=100,
        help_text=(
            'Optional title text, that will be shown when a user '
            'hovers over the link'
        )
    )
    separator = models.BooleanField(
        default=False,
        help_text='Select to include a separator after the previous link'
    )


class DCLNavbarPluginModel(CMSPlugin):
    logo_light = FilerImageField(
        on_delete=models.CASCADE, null=True, blank=True,
        help_text='Logo to be used on transparent navbar',
        related_name="dcl_navbar_logo_light",
    )
    logo_dark = FilerImageField(
        on_delete=models.CASCADE, null=True, blank=True,
        help_text='Logo to be used on white navbar',
        related_name="dcl_navbar_logo_dark",
    )
    logo_url = models.URLField(max_length=300, null=True, blank=True)
    language_dropdown = models.BooleanField(
        default=True,
        help_text='Select to include the language selection dropdown.'
    )

    def get_logo_dark(self):
        # used only if atleast one logo exists
        return self.logo_dark.url if self.logo_dark else self.logo_light.url

    def get_logo_light(self):
        # used only if atleast one logo exists
        return self.logo_light.url if self.logo_light else self.logo_dark.url


class DCLNavbarDropdownPluginModel(CMSPlugin):
    target = models.CharField(
        max_length=100, null=True, blank=True,
        help_text='Optional Url or #id to navigate on click'
    )
    text = models.CharField(
        max_length=50,
        help_text='Text for the dropdown toggle'
    )


class DCLContactPluginModel(CMSPlugin):
    heading = models.CharField(max_length=100, default="Contact", blank=True)
    organization_name = models.CharField(
        max_length=100, default="ungleich glarus ag", blank=True
    )
    email = models.EmailField(max_length=200, default="info@ungleich.ch")
    address = models.CharField(
        max_length=100, default="In der Au 7, Schwanden 8762", blank=True
    )
    country = models.CharField(
        max_length=100, default="Switzerland", blank=True
    )
    form_header = models.CharField(
        max_length=100, default="Send us a message.", blank=True
    )


class DCLFooterPluginModel(CMSPlugin):
    copyright_label = models.CharField(
        max_length=100, default='ungleich glarus ag', blank=True,
        help_text='Name of the company alongside the copyright year'
    )


class DCLSectionIconPluginModel(CMSPlugin):
    fontawesome_icon_name = models.CharField(
        max_length=30,
        help_text=mark_safe(
            'Name of the fontawesome icon to use. '
            '<a href="https://fontawesome.com/v4.7.0/icons/" target="_blank">'
            'Refer docs.</a>'
        )
    )


class DCLSectionImagePluginModel(CMSPlugin):
    image = FilerImageField(
        on_delete=models.CASCADE,
        help_text=(
            'Image file to be used in section. Add multiple plugins '
            'to add more than one image'
        )
    )
    caption = models.CharField(
        max_length=100, null=True, blank=True,
        help_text='Optional caption for the image.'
    )


class DCLSectionPromoPluginModel(CMSPlugin):
    background_image = FilerImageField(
        on_delete=models.CASCADE, null=True, blank=True,
        help_text=('Optional background image for the Promo Section'),
        related_name="dcl_section_promo_promo",
    )
    heading = models.CharField(
        blank=True, null=True, max_length=100,
        help_text='An optional heading for the Promo Section',
    )
    subheading = models.CharField(
        blank=True, null=True, max_length=200,
        help_text='An optional subheading for the Promo Section',
    )
    content = HTMLField()
    html_id = models.SlugField(
        blank=True, null=True,
        help_text=(
            'An optional html id for the Section. Required to set as target '
            'of a link on page'
        )
    )
    plain_heading = models.BooleanField(
        default=False,
        help_text='Select to keep the heading style simpler.'
    )
    text_center = models.BooleanField(
        default=False,
        help_text='Select to center align content on small screens.'
    )

    def __str__(self):
        return '#' + self.html_id if self.html_id else str(self.pk)

    def get_extra_classes(self):
        extra_classes = ''
        if self.text_center:
            extra_classes += ' text-center'
        if self.plain_heading:
            extra_classes += ' promo-section-plain'
        if self.background_image:
            extra_classes += ' promo-with-bg'
        return extra_classes


class MultipleChoiceArrayField(ArrayField):
    """
    A field that allows us to store an array of choices.
    Uses Django's Postgres ArrayField
    and a MultipleChoiceField for its formfield.
    """
    VMTemplateChoices = []
    if settings.OPENNEBULA_DOMAIN != 'test_domain':
        VMTemplateChoices = list(
            (
                str(obj.opennebula_vm_template_id),
                (obj.name + ' - ' + VMTemplate.IPV6.title()
                    if obj.vm_type == VMTemplate.IPV6 else obj.name
                 )
             )
            for obj in VMTemplate.objects.all()
        )

    def formfield(self, **kwargs):
        defaults = {
            'form_class': forms.MultipleChoiceField,
            'choices': self.VMTemplateChoices,
        }
        defaults.update(kwargs)
        # Skip our parent's formfield implementation completely as we don't
        # care for it.
        # pylint:disable=bad-super-call
        return super(ArrayField, self).formfield(**defaults)


class DCLCalculatorPluginModel(CMSPlugin):
    pricing = models.ForeignKey(
        VMPricing,
        related_name="dcl_custom_pricing_vm_pricing",
        help_text='Choose a pricing that will be associated with this '
                  'Calculator'
    )
    vm_type = models.CharField(
        max_length=50, choices=VMTemplate.VM_TYPE_CHOICES,
        default=VMTemplate.PUBLIC
    )
    vm_templates_to_show = MultipleChoiceArrayField(
        base_field=models.CharField(
            blank=True,
            max_length=256,
        ),
        default=list,
        blank=True,
        help_text="Recommended: If you wish to show all templates of the "
                  "corresponding VM Type (public/ipv6only), please do not "
                  "select any of the items in the above field. "
                  "This will allow any new template(s) added "
                  "in the backend to be automatically listed in this "
                  "calculator instance."
    )

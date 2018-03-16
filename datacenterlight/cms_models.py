from djangocms_text_ckeditor.fields import HTMLField
from cms.models.pluginmodel import CMSPlugin
from django.db import models
from django.utils.safestring import mark_safe
from filer.fields.image import FilerImageField

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
        help_text='Logo to be used on transparent navbar'
    )
    logo_dark = FilerImageField(
        on_delete=models.CASCADE, null=True, blank=True,
        help_text='Logo to be used on white navbar'
    )
    logo_url = models.URLField(max_length=300, null=True, blank=True)

    def get_logo_dark(self):
        # used only if atleast one logo exists
        return self.logo_dark.url if self.logo_dark else self.logo_white.url

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
        max_length=100, default="ungleich GmbH", blank=True
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
        max_length=100, default='ungleich GmbH', blank=True,
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

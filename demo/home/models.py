from django.db import models

from wagtail.models import Page

from wagtail.fields import StreamField
from wagtail.admin.panels import FieldPanel

from wagtail_photo_gallery.blocks import GalleryBlock
from wagtail_photo_gallery.mixins import ImageGalleryMixin


class HomePage(ImageGalleryMixin, Page):
    content = StreamField([
        #...
        ("gallery", GalleryBlock()),
        #...
    ], blank=True, use_json_field=True)
    
    # content panel for the CMS (same as always)
    content_panels = Page.content_panels + [
        FieldPanel("content"),
    ]
    
    

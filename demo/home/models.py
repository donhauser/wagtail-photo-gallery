from django.db import models

from wagtail.core.models import Page

from wagtail.core.fields import StreamField
from wagtail.admin.edit_handlers import StreamFieldPanel

from wagtail_photo_gallery.models import GalleryBlock, ImageGalleryMixin


class HomePage(ImageGalleryMixin, Page):
    content = StreamField([
        #...
        ("gallery", GalleryBlock()),
        #...
    ], blank=True)
    
    # content panel for the CMS (same as always)
    content_panels = Page.content_panels + [
        StreamFieldPanel("content"),
    ]
    
    

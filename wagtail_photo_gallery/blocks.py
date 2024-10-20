
from django.utils.functional import cached_property
from django.utils.translation import gettext_lazy as _

from wagtail import blocks
from wagtail.models import Collection
from wagtail.coreutils import resolve_model_string
from wagtail.models import get_root_collection_id

from .views import collection_chooser_viewset


GROUPING_CHOICES = [
        (None, _('Ungrouped')),
        ('year', _('Year')),
        #('month', 'Month'), # not implemented yet
        ('day', _('Day')),
    ]


_CollectionChooserBlock = collection_chooser_viewset.get_block_class()

class CollectionChooserBlock(_CollectionChooserBlock):
    
    class Meta:
        default=get_root_collection_id()


class GalleryBlock(blocks.StructBlock):
    
    title = blocks.CharBlock()
    collection = CollectionChooserBlock()
    ascending = blocks.BooleanBlock(required=False)
    grouping = blocks.ChoiceBlock(choices=GROUPING_CHOICES, default='year', required=False)
    
    @property
    def undated_albums_heading(self):
        return _("Undated Albums")
    
    def get_context(self, request, *args, **kwargs):
        
        context = super().get_context(request, *args, **kwargs)
        
        context["undated_albums_heading"] = self.undated_albums_heading
        
        return context
    
    class Meta:
        template = 'wagtail_photo_gallery/blocks/gallery_block.html'
        icon = 'image'

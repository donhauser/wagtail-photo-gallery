
from django.utils.functional import cached_property

from wagtail import blocks
from wagtail.models import Collection
from wagtail.coreutils import resolve_model_string
from wagtail.models import get_root_collection_id

from .views import collection_chooser_viewset


_CollectionChooserBlock = collection_chooser_viewset.get_block_class()

class CollectionChooserBlock(_CollectionChooserBlock):
    
    class Meta:
        default=get_root_collection_id()


class GalleryBlock(blocks.StructBlock):
    
    album_class = 'wagtail_photo_gallery.Album'
    
    title = blocks.CharBlock()
    collection = CollectionChooserBlock()
    # TODO order = ascending or descending
    # TODO grouping = choices: by month, year, none
    
    class Meta:
        template = 'wagtail_photo_gallery/blocks/gallery_block.html'
        icon = 'image'


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
    
    class Meta:
        template = 'wagtail_photo_gallery/blocks/photo_gallery.html'
        icon = 'image'
    
    @property
    def target_model(self):
        return resolve_model_string(self.album_class)
    
    
    def filter_albums(self, value):
        
        collection = value["collection"]
        query_set = collection.get_descendants(True) # get descendants INCLUDING the node itself
        
        return self.target_model.objects.filter(collection__in=query_set, is_visible=True)
    
    
    def get_context(self, request, *args, **kwargs):
        
        context = super().get_context(request, *args, **kwargs)
        
        context["albums"] = self.filter_albums(context["self"]).order_by('-created')
        
        return context

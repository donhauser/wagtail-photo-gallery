
from django.utils.functional import cached_property
from wagtail.core import blocks


from wagtail.core.utils import resolve_model_string


from .widgets import CollectionChooser

class CollectionChooserBlock(blocks.ChooserBlock):
    
    def get_form_state(self, value):
        # this function is required for wagtail > 2.12 (because it uses 'telepath')
        
        return self.widget.get_value_data(value)

    @property
    def target_model(self):
        return resolve_model_string('wagtailcore.Collection')
        
    @cached_property
    def widget(self):
        return CollectionChooser()

    class Meta:
        icon = "folder"

class GalleryBlock(blocks.StructBlock):
    
    album_class = 'wagtail_photo_gallery.Album'
    
    title = blocks.CharBlock()
    collection = CollectionChooserBlock()
    
    class Meta:
        template = 'blocks/photo_gallery.html'
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
        context["detail_url"] = "album/"
        
        return context

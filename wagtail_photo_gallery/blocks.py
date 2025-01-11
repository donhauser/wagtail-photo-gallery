
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

GALLERY_BLOCK_HELP_TEXTS = {
    'title': _("Display name of this gallery"),
    'collection': _("The gallery will show every album that belongs to the selected collection (and its descendants)"),
    'grouping': _("Organize the albums by date based grouping"),
    'ascending': _("Sort the album grouping in ascending order"),
}

_CollectionChooserBlock = collection_chooser_viewset.get_block_class()

class CollectionChooserBlock(_CollectionChooserBlock):
    """
    ChooserBlock for wagtail.Collection
    
    Defaults to the root collection.
    """

    def get_default(self):
        """
        The default choice for the block is the root collection
        """
        return get_root_collection_id() if self.meta.default is None else super().get_default()
    
    class Meta:
        icon = "folder"


class GalleryBlock(blocks.StructBlock):
    """
    Block for embedding every album that belongs to the specified collection (and its descendants)
    """
    
    title = blocks.CharBlock(help_text=GALLERY_BLOCK_HELP_TEXTS['title'])
    collection = CollectionChooserBlock(help_text=GALLERY_BLOCK_HELP_TEXTS['collection'])
    grouping = blocks.ChoiceBlock(choices=GROUPING_CHOICES, default='year', required=False, help_text=GALLERY_BLOCK_HELP_TEXTS['grouping'])
    ascending = blocks.BooleanBlock(required=False, help_text=GALLERY_BLOCK_HELP_TEXTS['ascending'])
    
    @property
    def undated_albums_heading(self):
        """
        Fallback heading for albums without a specified date
        """
        
        return _("Undated Albums")
    
    def get_context(self, request, *args, **kwargs):
        """
        Get the context of the StructBlock and set 'undated_albums_heading'
        """
        
        context = super().get_context(request, *args, **kwargs)
        
        context["undated_albums_heading"] = self.undated_albums_heading
        
        return context
    
    class Meta:
        template = 'wagtail_photo_gallery/blocks/gallery_block.html'
        icon = 'image'

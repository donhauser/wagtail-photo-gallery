from django.utils.translation import gettext_lazy as _

from wagtail.admin.viewsets.chooser import ChooserViewSet
from wagtail.admin.viewsets.model import ModelViewSet
from wagtail.models import Collection

from .models import Album


class CollectionChooserViewSet(ChooserViewSet):
    """
    ChooserViewSet for wagtail collections
    """
    
    icon = 'folder'
    model = Collection
    page_title = _("Choose a collection")


class AlbumModelViewSet(ModelViewSet):
    """
    ModelViewSet for Album management
    """
    
    model = Album
    icon = 'image'
    menu_order = 800
    add_to_admin_menu = True
    copy_view_enabled = False
    list_display = ('title', 'date', 'place', 'album_cover', 'album_images', 'modified')
    list_filter = ('collection', 'is_visible') #'date', 'place', 'modified', 'created'
    search_fields = ('title', 'date', 'place')


collection_chooser_viewset = CollectionChooserViewSet("collection_chooser")
album_model_viewset = AlbumModelViewSet("wagtail_photo_gallery/album")

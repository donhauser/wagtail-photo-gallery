from django.utils.translation import gettext_lazy as _

from generic_chooser.views import ModelChooserViewSet

from wagtail_photo_gallery.blocks import CollectionChooserBlock

class CollectionChooserViewSet(ModelChooserViewSet):
    icon = 'folder'
    model = CollectionChooserBlock.target_model
    page_title = _("Choose a collection")
    per_page = 10
